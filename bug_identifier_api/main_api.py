from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from typing import Optional
import json
import js2py
from pycparser import c_parser
from llm_call import call_gemini_llm 
from typing import List
app = FastAPI()
from fastapi import FastAPI
from rate_limiter import SimpleRateLimiter

app = FastAPI()
app.add_middleware(SimpleRateLimiter, max_requests=10, period=60)

class CodeSnippet(BaseModel):
    language: constr(strip_whitespace=True, min_length=1)
    code: constr(strip_whitespace=True, min_length=1, max_length=2000)
    
    
class BugReport(BaseModel):
    language: str
    bug_type: Optional[str] = None
    description: str 
    suggestion: Optional[str] = None
def syntax_check(language: str, code: str) -> (bool, str):
    language = language.lower()
    if language == "python":
        try:
            compile(code, "<string>", "exec")
            return True, ""
        except SyntaxError as e:
            return False, f"Python SyntaxError: {e}"
    elif language in ("js", "javascript"):
        try:
            js2py.parse_js(code)
            return True, ""
        except Exception as e:
            return False, f"JavaScript SyntaxError: {e}"
    elif language == "c":
        try:
            parser = c_parser.CParser()
            parser.parse(code)
            return True, ""
        except Exception as e:
            return False, f"C SyntaxError: {e}"
    else:
      return False, f"Language '{language}' is not supported for syntax check."

async def analyze_code_with_gemini(language: str, code: str) -> str:
    
    if not code.strip():
        return json.dumps({
            "bug_type": None,
            "description": "No code provided.",
            "suggestion": "Please submit some code to analyze."
        })
    prompt = f"""
    Analyze the following {language} code for bugs.
    If you find a bug, classify it as one of: logic, runtime, edge-case, off-by-one, or syntax.
    Return your answer as a JSON object with keys:

    "bug_type"
    "description"
    "suggestion"
    If there is no error in the code, set:

    "bug_type": null
    "description": "no error"
    "suggestion": null
    """
    gemini_response = await call_gemini_llm(prompt)
    return gemini_response
    

@app.post("/find-bug", response_model=BugReport)
async def find_bug(snippet: CodeSnippet):
    if not snippet.code or not snippet.code.strip():
        raise HTTPException(status_code=400, detail="No code provided. Please submit some code to analyze.")
    if len(snippet.code.splitlines()) > 30:
        raise HTTPException(status_code=400, detail="Code must be 30 lines or fewer.")
    is_valid, syntax_msg = syntax_check(snippet.language, snippet.code)
    if not is_valid:
        return BugReport(
            language=snippet.language,
            bug_type="syntax",
            description=syntax_msg,
            suggestion="Please fix the syntax error before further analysis."
        )

    try:
        gemini_result = await analyze_code_with_gemini(snippet.language, snippet.code)
        try:
            bug_data = json.loads(gemini_result)
        except Exception:
              raise HTTPException(status_code=500, detail="Gemini response was not valid JSON.")
        return BugReport(language=snippet.language, **bug_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")
    
