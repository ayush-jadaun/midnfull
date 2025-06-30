import os
from fastapi import FastAPI, HTTPException, Path, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

from livekit_service import LiveKitService
from gemini_service import GeminiService
from elevenlabs_service import ElevenLabsService

app = FastAPI(title="Mental Health AI Backend - Minimal Test")

# Initialize services
livekit_service = LiveKitService()
gemini_service = GeminiService()
elevenlabs_service = ElevenLabsService()

# ----- Request/Response Schemas -----
class ConversationInput(BaseModel):
    transcribed_text: str

class ConversationOutput(BaseModel):
    reply_text: str
    audio_url: str

class TokenRequest(BaseModel):
    identity: str
    room: str

class TokenResponse(BaseModel):
    token: str

# ----- API Endpoints -----

@app.post("/conversation/{session_id}/process", response_model=ConversationOutput)
def process_conversation(
    session_id: str = Path(..., description="Session ID for the call"),
    body: ConversationInput = ...
):
    """
    Minimal endpoint: receives user transcribed text, replies with Gemini, returns TTS audio.
    No memory, no Redis/Postgres.
    """
    try:
        user_text = body.transcribed_text

        # 1. Analyze emotion/sentiment using Gemini (optional for minimal, but included)
        emotion = gemini_service.analyze_emotion(user_text)

        # 2. Generate empathetic reply text using Gemini
        reply_text = gemini_service.generate_reply([f"user: {user_text}"], emotion, [])

        # 3. Convert reply text to speech audio using ElevenLabs, return as file or URL
        audio_bytes = elevenlabs_service.text_to_speech(reply_text)
        audio_file_path = f"audio_responses/{session_id}_reply.mp3"
        os.makedirs("audio_responses", exist_ok=True)
        elevenlabs_service.save_audio_to_file(audio_bytes, audio_file_path)
        audio_url = f"/static/{session_id}_reply.mp3"  # For local dev, serve with StaticFiles

        return {"reply_text": reply_text, "audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/livekit/token", response_model=TokenResponse)
def get_livekit_token(body: TokenRequest):
    """
    Endpoint to generate a LiveKit access token for a user & room.
    """
    try:
        token = livekit_service.generate_token(identity=body.identity, room=body.room)
        return {"token": token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token error: {str(e)}")

@app.post("/elevenlabs/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Endpoint to transcribe audio using ElevenLabs Speech-to-Text.
    """
    try:
        audio_bytes = await file.read()
        text = elevenlabs_service.speech_to_text(audio_bytes)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

# Serve static files for audio responses (for local dev; in production, use object storage or CDN)
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="audio_responses"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)