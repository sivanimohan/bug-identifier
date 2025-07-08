# bug_identifier_api

A Python backend for automated bug identification and code analysis using AI (Gemini LLM). This module powers the **AI Bug Identifier** Streamlit application, providing logic for analyzing user-submitted code, detecting bugs, and returning actionable suggestions in real-time.

---

## Features

- **Multi-Language Support:** Analyze Python, Java, and C code for common bug types.
- **AI-Powered Bug Detection:** Uses Google Gemini LLM for advanced bug identification and suggestions.
- **Syntax Checking:** Performs static syntax checks before AI analysis.
- **Flexible Response Modes:** Supports developer-friendly and casual output tones.
- **Sample Cases:** Includes sample buggy code snippets and explanations for demonstration/testing.

---

## File Structure

```
bug_identifier_api/
├── __init__.py
├── analyzer.py         # Core logic for syntax check & LLM analysis
├── llm_call.py         # Abstraction to call Gemini (or other LLMs)
├── test_cases.py       # SampleCase dataclass and example buggy code snippets
├── requirements.txt    # Python dependencies
└── ...                 # Other utility files or modules
```

---

## Usage

This module is designed to be used by the [Streamlit UI](../streamlit_app/README.md) (see the main repo).

**Example integration:**
```python
from bug_identifier_api.analyzer import run_analysis

bug_type, desc, sugg = run_analysis(language, code, mode)
```

---

## Example

**Input:**
```json
{
  "language": "python",
  "code": "def foo():\n  return 1/0"
}
```
**Output:**
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
- [streamlit](https://streamlit.io/)
- Your Gemini LLM API credentials/config

Install with:
```bash
pip install -r requirements.txt
```

---

## Extending

- Add support for more languages by extending `analyzer.py`.
- Swap out the language model or prompt in `llm_call.py`.

---

## License

MIT License

---

**Empower your code reviews with instant, AI-driven bug detection!**
