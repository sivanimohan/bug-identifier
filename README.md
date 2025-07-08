# bug_identifier_api

A Python backend API for automated bug identification and code analysis using AI (Gemini LLM). This component is designed to power the **AI Bug Identifier** application, providing endpoints and logic for analyzing user-submitted code, detecting bugs, and returning actionable suggestions in real-time.

---

## Features

- **Multi-Language Support:** Analyze Python, Java, and C code for common bug types.
- **AI-Powered Bug Detection:** Uses Google Gemini LLM for advanced bug identification and suggestions.
- **Syntax Checking:** Performs fast static syntax checks before AI analysis.
- **Flexible Response Modes:** Supports developer-friendly and casual output tones.
- **Sample Cases:** Includes sample buggy code snippets and explanations for demonstration/testing.

---

## File Structure

```
bug_identifier_api/
├── __init__.py
├── main.py             # (Example) FastAPI/Flask entrypoint for API server
├── analyzer.py         # Core logic for syntax check & LLM analysis
├── llm_call.py         # Abstraction to call Gemini (or other LLMs)
├── test_cases.py       # SampleCase dataclass and example buggy code snippets
├── requirements.txt    # Python dependencies
└── ...                 # Other utility files or modules
```

---

## Quickstart

1. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2. **Run the API server:**
    (Example with FastAPI)
    ```bash
    uvicorn main:app --reload
    ```

3. **Send a request:**
    Use cURL, Postman, or the [AI Bug Identifier UI](../streamlit_app/README.md) to submit code for analysis.

---

## Example Usage

**Sample API Request (JSON):**
```json
{
  "language": "python",
  "code": "def foo():\n  return 1/0"
}
```

**Sample API Response:**
```json
{
  "bug_type": "runtime",
  "description": "Division by zero error.",
  "suggestion": "Check for zero before dividing."
}
```

---

## Configuration

- **Supported Languages:** Python, Java, C
- **Modes:** Developer-friendly, Casual (adjusts response tone)
- **LLM Service:** Gemini (see `llm_call.py` for configuration)

---

## Dependencies

- Python 3.8+
- [pycparser](https://pypi.org/project/pycparser/)
- [streamlit](https://streamlit.io/) (for UI, if needed)
- [fastapi](https://fastapi.tiangolo.com/) or [flask](https://flask.palletsprojects.com/) (for API)
- Your Gemini LLM API credentials/config

---

## Extending

- Add support for more languages by extending `analyzer.py`.
- Swap out the language model or prompt in `llm_call.py`.
- Integrate with the Streamlit UI for a full-stack experience.

---

## License

MIT License

---

**Empower your code reviews with instant, AI-driven bug detection!**
