import streamlit as st
import requests

st.set_page_config(page_title="🐞 AI-Powered Bug Identifier")

st.title("🐞 AI-Powered Bug Identifier")

language = st.selectbox("Language", ["python", "java", "c"])
mode = st.radio("Tone", ["developer-friendly", "casual"])

code = st.text_area("Paste your code snippet (≤30 lines)", height=200, key="code_input")

if st.button("Find Bug"):
    if not code.strip():
        st.warning("Please submit some code to analyze.")
    else:
        try:
            resp = requests.post(
                "http://localhost:8000/find-bug",  # Change to your FastAPI backend URL if different
                params={"mode": mode},
                json={"language": language, "code": code},
                timeout=20
            )
            if resp.status_code == 200:
                bug = resp.json()
                st.json(bug)
            else:
                try:
                    error = resp.json().get("detail", resp.text)
                except Exception:
                    error = resp.text
                st.error(f"Error: {error}")
        except Exception as e:
            st.error(f"Request failed: {str(e)}")