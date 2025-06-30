import os
import requests
from typing import Optional

# Example environment variable: ELEVENLABS_API_KEY="your_elevenlabs_api_key"
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your_elevenlabs_api_key")
ELEVENLABS_API_URL = os.getenv("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1")

class ElevenLabsService:
    """
    Service for interacting with ElevenLabs API for Speech-to-Text (STT) and Text-to-Speech (TTS).
    """

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or ELEVENLABS_API_KEY
        self.api_url = api_url or ELEVENLABS_API_URL
        self.headers = {
            "xi-api-key": self.api_key,
        }

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "Rachel",  # Default English female voice, change as needed
        model_id: str = "eleven_multilingual_v2",  # Change to match your ElevenLabs model
        output_format: str = "mp3"
    ) -> bytes:
        """
        Generate speech audio from text using ElevenLabs TTS API.
        Returns audio content (bytes).
        """
        url = f"{self.api_url}/text-to-speech/{voice_id}"
        payload = {
            "text": text,
            "model_id": model_id,
            "output_format": output_format
        }
        response = requests.post(
            url,
            json=payload,
            headers={**self.headers, "Content-Type": "application/json"},
            timeout=30
        )
        response.raise_for_status()
        return response.content

    def speech_to_text(
        self,
        audio_bytes: bytes,
        model_id: str = "latest",  # Change to actual model if needed
        language: str = "en"
    ) -> str:
        """
        Transcribe speech audio to text using ElevenLabs STT API.
        Returns the transcribed text.
        """
        url = f"{self.api_url}/speech-to-text"
        files = {
            "audio": ("audio.wav", audio_bytes, "audio/wav"),
        }
        data = {
            "model_id": model_id,
            "language": language
        }
        response = requests.post(
            url,
            headers=self.headers,
            files=files,
            data=data,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result.get("text", "")

    def save_audio_to_file(self, audio_bytes: bytes, file_path: str) -> str:
        """
        Saves the audio bytes to a local file and returns the file path.
        """
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        return file_path

# Example usage (for testing; remove/comment out in production)
if __name__ == "__main__":
    service = ElevenLabsService()
    # Synthesize speech and save to file
    text = "Hello, this is a test from ElevenLabs TTS."
    audio = service.text_to_speech(text)
    path = service.save_audio_to_file(audio, "output.mp3")
    print("Audio saved to:", path)