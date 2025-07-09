#Ini buat backend dari ollama ke frontend

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

# CORS so React can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev, restrict in production
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
        json={"model": "qwen2.5-coder:0.5b", "prompt": prompt.prompt, "stream": False}
    )
	#Kalau mau ganti model tinggal ganti nama modelnya aja
	#Contoh : "model": "llama3"
    return response.json()

