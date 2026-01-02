import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

app = FastAPI()

# Permette chiamate dal sito Odoo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # poi lo restringiamo
    allow_methods=["POST"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    password: str
    message: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    CHAT_PASSWORD = os.getenv("CHAT_PASSWORD")
    if not CHAT_PASSWORD or req.password != CHAT_PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="Missing OPENAI_API_KEY")

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Sei un assistente tecnico interno per manutenzione "
                        "di apparecchiature odontoiatriche. "
                        "Rispondi in italiano, in modo pratico e operativo."
                    ),
                },
                {"role": "user", "content": req.message},
            ],
        )
