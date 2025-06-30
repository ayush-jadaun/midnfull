import os
import requests
from typing import List, Dict, Any

# Load Gemini API credentials from environment variables or use defaults for development/testing
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC9fQJwRJ06tnCTvJzI67aJJD78w6_hOLE")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent")

class GeminiService:
    """
    Service for interacting with Google's Gemini LLM API for
    emotion analysis, response generation, and (placeholder) embeddings.
    """

    def __init__(self, api_key: str = None, api_url: str = None):
        # Initialize with provided API key and URL, or use defaults
        self.api_key = api_key or GEMINI_API_KEY
        self.api_url = api_url or GEMINI_API_URL

    def _headers(self) -> Dict[str, str]:
        # Prepare HTTP headers for Gemini API requests
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

    def analyze_emotion(self, text: str) -> str:
        """
        Analyze the user's emotion from input text using Gemini.
        Returns a single-word emotion label in lowercase.
        """
        prompt = (
            "Analyze the following text and respond ONLY with a single word that best describes the user's emotion "
            "(e.g., angry, sad, happy, neutral, anxious, etc.):\n\n"
            f"{text}"
        )
        response = self._call_gemini(prompt)
        return response.strip().lower()

    def generate_reply(self, conversation: List[str], emotion: str, memories: List[Dict[str, Any]]) -> str:
        """
        Generate an empathetic reply based on conversation history, detected emotion, and relevant memories.
        - conversation: list of recent utterances (["user: ...", "ai: ...", ...])
        - emotion: detected emotion label
        - memories: list of dicts with memory summaries
        """
        context = "\n".join(conversation)
        memory_summaries = "\n".join([m["summary"] for m in memories]) if memories else ""
        prompt = (
            f"You are an empathetic mental health assistant. The user's detected emotion is: {emotion}.\n"
            f"Recent conversation:\n{context}\n"
            f"Relevant past memories:\n{memory_summaries}\n"
            "Reply in a way that is supportive, non-judgmental, and encourages the user to share more if they wish."
        )
        return self._call_gemini(prompt)

    def get_embedding(self, text: str) -> List[float]:
        """
        Placeholder for text embedding functionality.
        Currently returns a random vector; replace with actual embedding API as needed.
        """
        import numpy as np
        VECTOR_DIM = 1536
        return np.random.rand(VECTOR_DIM).astype(float).tolist()

    def _call_gemini(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the generated text response.
        Handles API errors gracefully.
        """
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        resp = requests.post(
            self.api_url,
            headers={"Content-Type": "application/json"},
            params={"key": self.api_key},
            json=payload,
            timeout=20
        )
        try:
            resp.raise_for_status()
            data = resp.json()
            # Extract the generated text from Gemini's response
            return (
                data["candidates"][0]["content"]["parts"][0]["text"]
                if data.get("candidates") else ""
            )
        except Exception as e:
            print(f"Gemini API error: {e} | Response: {resp.text}")
            return ""

# Example usage for local development/testing
if __name__ == "__main__":
    service = GeminiService()
    print("Emotion:", service.analyze_emotion("I'm so frustrated with my job lately."))
    print("Reply:", service.generate_reply(
        ["user: I'm so frustrated with my job lately."],
        "frustrated",
        []
    ))