from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, constr
from typing import Optional, List
import json
import subprocess
from pycparser import c_parser
from llm_call import call_gemini_llm 
from test_cases import SampleCase, sample_cases

app = FastAPI()

class CodeSnippet(BaseModel):
    language: constr(strip_whitespace=True, min_length=1)
    code: constr(strip_whitespace=True, min_length=1, max_length=2000)

class BugReport(BaseModel):
    language: str
    bug_type: Optional[str] = None
    description: str 
    suggestion: Optional[str] = None

def check_java_syntax(code: str) -> tuple[bool, str]:
    try:
        import tempfile, os
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, 'Main.java')
        with open(file_path, "w") as f:
            f.write(code)
        result = subprocess.run(
            ["javac", file_path],
            capture_output=True,
            text=True
        )
        os.remove(file_path)
        os.rmdir(temp_dir)
        if result.returncode == 0:
            return True, ""
        else:
            return False, f"Java SyntaxError: {result.stderr.strip()}"
    except Exception as e:
        return False, f"Java Syntax check failed: {e}"

def syntax_check(language: str, code: str) -> tuple[bool, str]:
    language = language.lower()
    if language == "python":
        try:
            compile(code, "<string>", "exec")
            return True, ""
        except SyntaxError as e:
            return False, f"Python SyntaxError: {e}"
    elif language == "java":
        return check_java_syntax(code)
    elif language == "c":
        try:
            parser = c_parser.CParser()
            parser.parse(code)
            return True, ""
        except Exception as e:
            return False, f"C SyntaxError: {e}"
    else:
        return False, f"Language '{language}' is not supported for syntax check."

async def analyze_code_with_gemini(language: str, code: str, mode: str = "developer-friendly") -> str:
    if not code.strip():
        return json.dumps({
            "bug_type": None,
            "description": "No code provided.",
            "suggestion": "Please submit some code to analyze."
        })

    if mode == "casual":
        tone_instruction = (
            "Respond in a friendly, casual tone. "
            "Write the description and suggestion as simple, one-line explanations."
        )
    else:
        tone_instruction = (
            "Respond in a concise, developer-friendly tone. "
            "Write the description and suggestion as clear, single-line explanations."
        )

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

    {tone_instruction}

    Code:
    {code}
    """
    gemini_response = await call_gemini_llm(prompt)
    return gemini_response

@app.post("/find-bug", response_model=BugReport)
async def find_bug(
    snippet: CodeSnippet,
    mode: str = Query("developer-friendly", enum=["developer-friendly", "casual"])
):
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
        gemini_result = await analyze_code_with_gemini(snippet.language, snippet.code, mode)
        try:
            bug_data = json.loads(gemini_result)
        except Exception:
            raise HTTPException(status_code=500, detail="Gemini response was not valid JSON.")
        return BugReport(language=snippet.language, **bug_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing code: {str(e)}")
    
@app.get("/sample-cases", response_model=List[SampleCase])
async def get_sample_cases():
    return sample_cases

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    import nest_asyncio
    nest_asyncio.apply()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)