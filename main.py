from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

AI_TOKEN = "TOKEN_LUNGO_E_CASUALE"

@app.post("/chat")
async def chat(payload: dict, x_ai_token: str = Header(None)):
    if x_ai_token != AI_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = payload.get("message")
    if not message:
        raise HTTPException(status_code=400, detail="Missing message")

    return {
        "reply": f"Ricevuto: {message}"
    }
