# Bug Identifier

**Bug Identifier** is an AI-powered tool for automatically detecting bugs in your code snippets. Built using Python and Streamlit, it leverages Gemini LLM for instant bug analysis and actionable suggestions for Python, Java, and C code.

---

## Features

- **AI-driven bug detection:** Uses Gemini LLM to classify bugs (logic, runtime, edge-case, off-by-one, syntax) and suggest fixes.
- **Multi-language support:** Python, Java, and C code.
- **Local syntax checking:** Fast static validation before AI analysis.
- **Flexible tone:** Developer-friendly or casual output.
- **Sample cases:** Built-in buggy code examples.
- **Streamlit web app:** Intuitive, interactive UI.

---

## Directory Structure

```
bug-identifier/
├── bug_identifier_api/
│   ├── analyzer.py
│   ├── llm_call.py
│   ├── main.py          # Main Streamlit app (entry point)
│   ├── test_cases.py
│   ├── static/
│   ├── __pycache__/
│   └── requirements.txt
├── README.md
└── ...
```

---

## Getting Started

1. **Install dependencies**
    ```bash
    pip install -r bug_identifier_api/requirements.txt
    ```

2. **Run the Streamlit app**
    ```bash
    streamlit run bug_identifier_api/main.py
    ```

---

## Usage

- Paste your code in the editor.
- Select the language (Python, Java, or C).
- Choose the tone ("developer-friendly" or "casual").
- Click "Find Bug" for instant feedback and suggestions.
- Try "Sample Cases" for quick demos.

---

## Example

**Input:**
```python
def foo():
    return 1/0
```

**Output:**
- **Bug Type:** runtime
- **Description:** Division by zero error.
- **Suggestion:** Check for zero before dividing.

---

## Configuration

- **Supported Languages:** Python, Java, C
- **Modes:** Developer-friendly, Casual (response tone)
- **LLM Service:** Gemini (API key required, see `llm_call.py`)
- **Extending:** Add new languages or bug types in `analyzer.py` and `test_cases.py`.

---

## License

MIT License

---

**Instant, AI-powered bug detection for your code.**
