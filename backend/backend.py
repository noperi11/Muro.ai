from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# Aktifkan CORS supaya React dev server bisa akses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # hanya React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Prompt(BaseModel):
    prompt: str

@app.post("/chat")
def chat(prompt: Prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "deepseek-coder-v2:16b", "prompt": prompt.prompt, "stream": False}
    )
    return response.json()
