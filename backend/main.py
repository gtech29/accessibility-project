from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.1:8b-instruct-q8_0"

SYSTEM_PROMPT = """
You are an ASL interpretation engine.
You will receive raw ASL letter sequences with no spaces and simplified grammar.
Your task is to:
- Infer correct word boundaries.
- Add necessary English helper words.
- Convert the message into natural, grammatically correct, expressive English.
Preserve the intended meaning.
Return only the final English sentence. Do not explain. Do not add extra text.
"""

class ASLRequest(BaseModel):
    raw_asl: str

@app.post("/interpret")
def interpret_asl(data: ASLRequest):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": data.raw_asl}
    ]

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
    )

    result = response.json()
    return result