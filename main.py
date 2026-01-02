from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import openai

# =====================
# CONFIG
# =====================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AI_WEB_TOKEN = os.getenv("AI_WEB_TOKEN")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY non impostata")

openai.api_key = OPENAI_API_KEY

# =====================
# APP
# =====================

app = FastAPI()

# 🔴 CORS – FONDAMENTALE PER ODOO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puoi restringere dopo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# MODELS
# =====================

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# =====================
# ROUTES
# =====================

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat(
    data: ChatRequest,
    x_ai_token: str = Header(None)
):
    # 🔐 Sicurezza token
    if x_ai_token != AI_WEB_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Sei un assistente tecnico per manutenzione e assistenza."
                },
                {
                    "role": "user",
                    "content": data.message
                }
            ],
            temperature=0.2,
        )

        reply = response.choices[0].message["content"]
        return {"reply": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
