import aiohttp
import json
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Gemini API error {resp.status}: {text}")
            result = await resp.json()
            try:
                reply = result['candidates'][0]['content']['parts'][0]['text']
                # Try to parse as JSON to ensure it is valid
                json.loads(reply)
                return reply
            except Exception:
                return json.dumps({
                    "bug_type": None,
                    "description": "Gemini did not return a valid JSON response.",
                    "suggestion": None
                })