import os
import requests
from typing import List, Dict, Any

# Example environment variable: GEMINI_API_KEY="your_gemini_api_key"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyC9fQJwRJ06tnCTvJzI67aJJD78w6_hOLE")
GEMINI_API_URL = os.getenv("GEMINI_API_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent")

class GeminiService:
    """
    Service for interacting with Google's Gemini LLM API for
    emotion analysis, response generation, and embeddings (if available).
    """

    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key or GEMINI_API_KEY
        self.api_url = api_url or GEMINI_API_URL

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

    def analyze_emotion(self, text: str) -> str:
        """
        Uses Gemini to analyze the emotion or sentiment of the input text.
        Returns a single emotion label (e.g. "angry", "sad", "neutral", etc.).
        """
        prompt = f"Analyze the following text and respond ONLY with a single word that best describes the user's emotion (e.g., angry, sad, happy, neutral, anxious, etc.):\n\n{text}"
        response = self._call_gemini(prompt)
        return response.strip().lower()

    def generate_reply(self, conversation: List[str], emotion: str, memories: List[Dict[str, Any]]) -> str:
        """
        Uses Gemini to generate an empathetic reply based on conversation history, detected emotion, and long-term memories.
        `conversation`: list of recent utterances (["user: ...", "ai: ...", ...])
        `emotion`: detected emotion/sentiment
        `memories`: list of dicts with summaries from long-term memory
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
        Placeholder for Gemini text embedding; Gemini does not provide public embeddings API as of June 2024.
        Replace this with your actual embedding API (e.g., OpenAI, Vertex AI, etc.).
        """
        # TODO: Replace with actual embedding call.
        import numpy as np
        VECTOR_DIM = 1536
        return np.random.rand(VECTOR_DIM).astype(float).tolist()

    def _call_gemini(self, prompt: str) -> str:
        """
        Helper to make a chat/completion call to Gemini.
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
            # Gemini's response format:
            # data["candidates"][0]["content"]["parts"][0]["text"]
            return (
                data["candidates"][0]["content"]["parts"][0]["text"]
                if data.get("candidates") else ""
            )
        except Exception as e:
            print(f"Gemini API error: {e} | Response: {resp.text}")
            return ""

# Example usage (for local/dev test)
if __name__ == "__main__":
    service = GeminiService()
    print("Emotion:", service.analyze_emotion("I'm so frustrated with my job lately."))
    print("Reply:", service.generate_reply(
        ["user: I'm so frustrated with my job lately."],
        "frustrated",
        []
    ))