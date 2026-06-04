from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from groq import Groq
import os
import json

app = FastAPI(title="eFootball AI Coach Website")

# Mount static files if needed later
# app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== GROQ API KEY ====================
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
# =====================================================

SYSTEM_PROMPT = """You are "eFootball Guru" — expert eFootball 2025/2026 coach. 
Give detailed, actionable advice on formations, players, tactics. 
Reply in Bangla if user asks in Bangla/Banglish, otherwise English.
Be friendly and helpful. Use football terms like CF, AMF, Quick Counter etc."""

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat_endpoint(request: Request):
    try:
        body = await request.json()
        user_message = body.get("message", "")
        history = body.get("history", [])
        
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        for msg in history[-6:]:  # Keep last 6 messages for context
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.65,
            max_tokens=1200,
        )
        
        reply = completion.choices[0].message.content.strip()
        
        return JSONResponse({
            "reply": reply,
            "success": True
        })
        
    except Exception as e:
        return JSONResponse({
            "error": str(e),
            "success": False
        }, status_code=500)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting eFootball AI Website...")
    print("   Open http://127.0.0.1:8000 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8000)
