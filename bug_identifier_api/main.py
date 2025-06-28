import streamlit as st
import json
import subprocess
from pycparser import c_parser
from typing import Optional
from llm_call import call_gemini_llm  
from test_cases import SampleCase, sample_cases  

st.title("AI Bug Identifier")
st.write("Paste your code, choose a language and mode, and find bugs instantly!")

def check_java_syntax(code: str):
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

def syntax_check(language: str, code: str):
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

async def analyze_code_with_gemini(language: str, code: str, mode: str = "developer-friendly"):
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
    IMPORTANT: Respond ONLY with the JSON object and nothing else.
    {tone_instruction}

    Code:
    {code}
    """
    gemini_response = await call_gemini_llm(prompt)
    return gemini_response

def run_analysis(language, code, mode):
    if not code or not code.strip():
        return "No code provided.", "", ""
    if len(code.splitlines()) > 30:
        return "Code must be 30 lines or fewer.", "", ""
    is_valid, syntax_msg = syntax_check(language, code)
    if not is_valid:
        return f"Syntax Error: {syntax_msg}", "", "Please fix the syntax error before further analysis."
    try:
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        gemini_result = loop.run_until_complete(analyze_code_with_gemini(language, code, mode))
        bug_data = json.loads(gemini_result)
        bug_type = bug_data.get("bug_type", "")
        desc = bug_data.get("description", "")
        sugg = bug_data.get("suggestion", "")
        return bug_type, desc, sugg
    except Exception as e:
        return "Error", f"Error analyzing code: {str(e)}", ""


LANGUAGES = ["python", "java", "c"]
language = st.selectbox("Language", LANGUAGES, index=0)
code = st.text_area("Code", height=300)
mode = st.radio("Mode", ["developer-friendly", "casual"], index=0)

if st.button("Find Bug"):
    bug_type, desc, sugg = run_analysis(language, code, mode)
    st.write(f"**Bug Type:** {bug_type}")
    st.write(f"**Description:** {desc}")
    st.write(f"**Suggestion:** {sugg}")

with st.expander("Sample Cases"):
    if hasattr(sample_cases, "__iter__"):
        for case in sample_cases:
            st.code(case.code, language=case.language)
            st.write(f"**Description:** {case.description}")
            st.write(f"**Suggestion:** {case.suggestion}")
    else:
        st.info("No sample cases available.")