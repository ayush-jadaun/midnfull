import os
import requests
from typing import Optional

# Load ElevenLabs API credentials from environment variables, or use defaults for development/testing
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "sk_5fb10beefb932a890e6fe6e5133434738275a49da7dca69b")
ELEVENLABS_API_URL = os.getenv("ELEVENLABS_API_URL", "https://api.elevenlabs.io/v1")

class ElevenLabsService:
    """
    Service for interacting with the ElevenLabs API for both text-to-speech (TTS) and speech-to-text (STT).
    """

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        # Allow overriding API key and URL, otherwise use environment/defaults
        self.api_key = api_key or ELEVENLABS_API_KEY
        self.api_url = api_url or ELEVENLABS_API_URL
        self.headers = {
            "xi-api-key": self.api_key,
        }

    def text_to_speech(
        self,
        text: str,
        voice_id: str = "Rachel",
        model_id: str = "eleven_multilingual_v2",
        output_format: str = "mp3"
    ) -> bytes:
        """
        Convert text to speech using ElevenLabs TTS API.
        Returns the generated audio as bytes.
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
        model_id: str = "latest",
        language: str = "en"
    ) -> str:
        """
        Transcribe audio bytes to text using ElevenLabs STT API.
        Returns the recognized text.
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
        Save audio bytes to a file on disk.
        Returns the path to the saved file.
        """
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        return file_path

# Example usage for local testing
if __name__ == "__main__":
    service = ElevenLabsService()
    # Generate speech from text and save the audio to a file
    text = "Hello, this is a test from ElevenLabs TTS."
    audio = service.text_to_speech(text)
    path = service.save_audio_to_file(audio, "output.mp3")
    print("Audio saved to:", path)