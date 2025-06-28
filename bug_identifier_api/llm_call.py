import aiohttp
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def extract_json_from_text(text):
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return None

async def call_gemini_llm(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment.")
    headers = {
        "Content-Type": "application/json"
    }
    params = {"key": GEMINI_API_KEY}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_API_URL, params=params, headers=headers, json=data) as resp:
            response_json = await resp.json()
            if resp.status != 200:
               
                return json.dumps({
                    "bug_type": "Error",
                    "description": f"Gemini API error {resp.status}: {json.dumps(response_json)}",
                    "suggestion": None
                })
            try:
                reply = response_json['candidates'][0]['content']['parts'][0]['text']
               
                bug_data = extract_json_from_text(reply)
                if bug_data:
                    return json.dumps(bug_data)
                else:
                   
                    return json.dumps({
                        "bug_type": None,
                        "description": reply,
                        "suggestion": None
                    })
            except Exception as e:
                return json.dumps({
                    "bug_type": None,
                    "description": f"Could not parse Gemini response: {str(e)}",
                    "suggestion": None
                })