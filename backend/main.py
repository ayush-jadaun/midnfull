import os
import uuid
from typing import List, Optional

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
import redis
import psycopg2
import requests

# ---------------------- Configuration & Setup ---------------------- #

# Environment variable placeholders (replace with your real secrets in production)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your-11labs-api-key")
LLM_API_KEY = os.getenv("LLM_API_KEY", "your-llm-api-key")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_DB = os.getenv("PG_DB", "mentalhealth")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "postgres")
PG_PORT = int(os.getenv("PG_PORT", 5432))

# Number of messages to store in short-term memory
SHORT_TERM_MEM_LIMIT = 10

# Redis connection
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# PostgreSQL connection
pg_conn = psycopg2.connect(
    host=PG_HOST, dbname=PG_DB, user=PG_USER, password=PG_PASSWORD, port=PG_PORT
)
pg_conn.autocommit = True

# ---------------------- FastAPI Setup ---------------------- #

app = FastAPI(
    title="Mental Health AI Conversation API",
    description="AI Listens and responds to user emotions in real time",
    version="1.0.0"
)

# ---------------------- Models ---------------------- #

class ConversationRequest(BaseModel):
    transcribed_text: str

class ConversationResponse(BaseModel):
    reply_text: str
    audio_url: str

# ---------------------- Redis Short-term Memory ---------------------- #

def get_short_term_memory(session_id: str) -> List[str]:
    """Retrieve last N messages for session from Redis."""
    return redis_client.lrange(f"session:{session_id}:messages", 0, -1)

def add_message_to_short_term_memory(session_id: str, text: str):
    """Push message to Redis short-term memory list."""
    key = f"session:{session_id}:messages"
    redis_client.rpush(key, text)
    redis_client.ltrim(key, -SHORT_TERM_MEM_LIMIT, -1)

def clear_short_term_memory(session_id: str):
    """Clear session memory in Redis (optional, not used here)."""
    redis_client.delete(f"session:{session_id}:messages")

# ---------------------- Postgres Long-term Memory ---------------------- #

def store_long_term_memory(session_id: str, summary: str):
    """Save summary to Postgres for the session."""
    with pg_conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversation_longterm (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                session_id TEXT,
                summary TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute(
            "INSERT INTO conversation_longterm (session_id, summary) VALUES (%s, %s)",
            (session_id, summary)
        )

def get_long_term_memory(session_id: str) -> Optional[str]:
    """Get last summary for session from Postgres."""
    with pg_conn.cursor() as cur:
        cur.execute(
            "SELECT summary FROM conversation_longterm WHERE session_id=%s ORDER BY created_at DESC LIMIT 1",
            (session_id,)
        )
        row = cur.fetchone()
        return row[0] if row else None

# ---------------------- ElevenLabs API Integration ---------------------- #

def elevenlabs_tts(text: str) -> str:
    """Generate speech from text using ElevenLabs API. Returns a URL or path to audio file."""
    url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"  # Replace with your voice_id or config
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }
    # For demo, we just simulate and return a placeholder
    # In production, POST to ElevenLabs and return audio file URL you host or a presigned URL.
    # resp = requests.post(url, headers=headers, json=data)
    # audio_url = resp.json().get("audio_url")  # Adapt depending on API response
    audio_url = f"https://your-storage.example.com/audio/{uuid.uuid4()}.mp3"
    return audio_url

def elevenlabs_stt(audio_url: str) -> str:
    """Transcribe audio from URL using ElevenLabs API (not used in this backend, but provided for completeness)."""
    # Placeholder for actual implementation
    return "Transcribed text"

# ---------------------- LLM Integration (Gemini/Other) ---------------------- #

def analyze_emotion(text: str) -> str:
    """Analyze the emotion or sentiment of the text using LLM."""
    # Call to Gemini or other LLM here (pseudo-code)
    # resp = requests.post(LLM_URL, headers={"Authorization": f"Bearer {LLM_API_KEY}"}, json={"text": text})
    # return resp.json().get("emotion")
    # Placeholder:
    return "empathetic"

def generate_llm_reply(messages: List[str], emotion: str, long_memory: Optional[str]) -> str:
    """Generate an empathetic reply using LLM with context from memory and emotion."""
    # Here you would call Gemini or another LLM, passing the last messages and emotion context
    # For demonstration, return a simple string
    context = ""
    if long_memory:
        context += f"Long-term memory: {long_memory}\n"
    context += "\n".join(messages[-SHORT_TERM_MEM_LIMIT:])
    # resp = requests.post(..., json={"messages": context, "emotion": emotion})
    # return resp.json().get("reply")
    return f"I hear you. It sounds like you're feeling {emotion}. I'm here to listen and support you."

def summarize_for_long_term(messages: List[str]) -> str:
    """Summarize conversation for long-term memory (placeholder)."""
    # You could call an LLM or use simple logic to summarize
    return "Summary of your recent venting session."

# ---------------------- FastAPI Endpoint ---------------------- #

@app.post("/conversation/{session_id}/process", response_model=ConversationResponse)
def process_conversation(
    session_id: str = Path(..., description="Session identifier"),
    req: ConversationRequest = None
):
    # 1. Receive transcribed text
    transcribed_text = req.transcribed_text.strip()
    if not transcribed_text:
        raise HTTPException(status_code=400, detail="transcribed_text cannot be empty")

    # 2. Analyze emotion/sentiment
    emotion = analyze_emotion(transcribed_text)

    # 3. Store in Redis (short-term memory)
    add_message_to_short_term_memory(session_id, transcribed_text)
    short_memory = get_short_term_memory(session_id)

    # 4. Retrieve long-term memory (if any)
    long_term = get_long_term_memory(session_id)

    # 5. Generate empathetic reply via LLM
    reply_text = generate_llm_reply(short_memory, emotion, long_term)

    # 6. Optionally, store summary in Postgres (long-term memory)
    summary = summarize_for_long_term(short_memory)
    store_long_term_memory(session_id, summary)

    # 7. Convert reply to speech via ElevenLabs
    audio_url = elevenlabs_tts(reply_text)

    # 8. Return reply text and audio URL
    return ConversationResponse(reply_text=reply_text, audio_url=audio_url)

# ---------------------- Example: Environment Variables ---------------------- #
"""
# .env example (do not commit secrets)
ELEVENLABS_API_KEY=pk-xxx
LLM_API_KEY=sk-xxx
REDIS_URL=redis://localhost:6379/0
PG_HOST=localhost
PG_DB=mentalhealth
PG_USER=postgres
PG_PASSWORD=postgres
PG_PORT=5432
"""

# ---------------------- Run the App (for local dev) ---------------------- #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)