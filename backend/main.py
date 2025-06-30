import os
from fastapi import FastAPI, HTTPException, Path, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn
import traceback

from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

try:
    from services.livekit_service import LiveKitService
    from services.gemini_service import GeminiService
    from services.eleven_labs import ElevenLabsService
except ImportError as e:
    print(f"Warning: Could not import some services: {e}")
    # Create placeholder services for testing
    class LiveKitService:
        def generate_token(self, identity: str, room: str, **kwargs):
            return "mock-token-for-testing"
    
    class GeminiService:
        def analyze_emotion(self, text: str):
            return "neutral"
        
        def generate_reply(self, conversation: list, emotion: str, context: list):
            return "I understand how you're feeling. Let's talk about it."
    
    class ElevenLabsService:
        def text_to_speech(self, text: str):
            return b"mock-audio-data"
        
        def save_audio_to_file(self, audio_bytes: bytes, path: str):
            pass
        
        def speech_to_text(self, audio_bytes: bytes):
            return "Mock transcription"

app = FastAPI(title="Mental Health AI Backend - Audio Calls")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with error handling
try:
    livekit_service = LiveKitService()
    print("✅ LiveKit service initialized successfully")
except Exception as e:
    print(f"❌ Error initializing LiveKit service: {e}")
    livekit_service = None

try:
    gemini_service = GeminiService()
    print("✅ Gemini service initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Gemini service: {e}")
    gemini_service = None

try:
    elevenlabs_service = ElevenLabsService()
    print("✅ ElevenLabs service initialized successfully")
except Exception as e:
    print(f"❌ Error initializing ElevenLabs service: {e}")
    elevenlabs_service = None

# ----- Request/Response Schemas -----
class ConversationInput(BaseModel):
    transcribed_text: str

class ConversationOutput(BaseModel):
    reply_text: str
    audio_url: str

class TokenResponse(BaseModel):
    token: str

# ----- Health Check Endpoint -----
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "livekit": livekit_service is not None,
            "gemini": gemini_service is not None,
            "elevenlabs": elevenlabs_service is not None,
        }
    }

# ----- LiveKit Token Endpoint -----
@app.post("/livekit/token/{room_id}", response_model=TokenResponse)
def get_livekit_token_by_room(
    room_id: str = Path(..., description="Room ID for the call"),
    user_id: str = Query(..., description="User ID for the participant")
):
    """
    Generate a LiveKit access token for audio-only calls.
    """
    try:
        print(f"🔑 Generating token for user '{user_id}' in room '{room_id}'")
        
        if not livekit_service:
            raise HTTPException(
                status_code=503, 
                detail="LiveKit service is not available. Check LIVEKIT_API_KEY and LIVEKIT_API_SECRET environment variables."
            )
        
        # Validate inputs
        if not room_id or not user_id:
            raise HTTPException(
                status_code=400,
                detail="Both room_id and user_id are required"
            )
        
        # Generate token with audio-only permissions
        token = livekit_service.generate_token(
            identity=user_id, 
            room=room_id,
            can_publish_audio=True,
            can_subscribe_audio=True,

        )
        
        print(f"✅ Token generated successfully for user '{user_id}'")
        return {"token": token}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating token: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate LiveKit token: {str(e)}"
        )

# ----- Conversation Processing Endpoint -----
@app.post("/conversation/{session_id}/process", response_model=ConversationOutput)
def process_conversation(
    session_id: str = Path(..., description="Session ID for the call"),
    body: ConversationInput = ...
):
    """
    Process user speech: transcribe -> analyze -> generate reply -> convert to speech
    """
    try:
        print(f"💬 Processing conversation for session '{session_id}'")
        
        if not gemini_service or not elevenlabs_service:
            raise HTTPException(
                status_code=503,
                detail="Required services are not available"
            )
        
        user_text = body.transcribed_text
        print(f"📝 User text: {user_text}")
        
        # 1. Analyze emotion/sentiment
        emotion = gemini_service.analyze_emotion(user_text)
        print(f"😊 Detected emotion: {emotion}")
        
        # 2. Generate empathetic reply
        reply_text = gemini_service.generate_reply([f"user: {user_text}"], emotion, [])
        print(f"🤖 Generated reply: {reply_text}")
        
        # 3. Convert to speech
        audio_bytes = elevenlabs_service.text_to_speech(reply_text)
        
        # 4. Save audio file
        audio_dir = "audio_responses"
        os.makedirs(audio_dir, exist_ok=True)
        audio_file_path = f"{audio_dir}/{session_id}_reply.mp3"
        elevenlabs_service.save_audio_to_file(audio_bytes, audio_file_path)
        
        audio_url = f"/static/{session_id}_reply.mp3"
        
        print(f"🎵 Audio saved to: {audio_url}")
        
        return {
            "reply_text": reply_text, 
            "audio_url": audio_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing conversation: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to process conversation: {str(e)}"
        )

# ----- Audio Transcription Endpoint -----
@app.post("/elevenlabs/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio using ElevenLabs Speech-to-Text.
    """
    try:
        print(f"🎤 Transcribing audio file: {file.filename}")
        
        if not elevenlabs_service:
            raise HTTPException(
                status_code=503,
                detail="ElevenLabs service is not available"
            )
        
        audio_bytes = await file.read()
        text = elevenlabs_service.speech_to_text(audio_bytes)
        
        print(f"📝 Transcription result: {text}")
        return {"text": text}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error transcribing audio: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to transcribe audio: {str(e)}"
        )

# ----- Static Files -----
AUDIO_DIR = "audio_responses"
os.makedirs(AUDIO_DIR, exist_ok=True)

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory=AUDIO_DIR), name="static")

# ----- Debug Endpoint -----
@app.get("/debug/env")
def debug_environment():
    """Debug endpoint to check environment variables (remove in production)"""
    return {
        "livekit_api_key_set": bool(os.getenv("LIVEKIT_API_KEY")),
        "livekit_api_secret_set": bool(os.getenv("LIVEKIT_API_SECRET")),
        "livekit_ws_url": os.getenv("LIVEKIT_WS_URL", "Not set"),
        "python_path": os.getenv("PYTHONPATH", "Not set"),
    }

if __name__ == "__main__":
    print("🚀 Starting Mental Health AI Backend...")
    print("📋 Environment check:")
    print(f"   LIVEKIT_API_KEY: {'✅ Set' if os.getenv('LIVEKIT_API_KEY') else '❌ Not set'}")
    print(f"   LIVEKIT_API_SECRET: {'✅ Set' if os.getenv('LIVEKIT_API_SECRET') else '❌ Not set'}")
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)), 
        reload=True,
        log_level="info"
    )