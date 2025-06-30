import os
import time
import jwt  # PyJWT library: pip install PyJWT

# Example environment variable placeholders
# LIVEKIT_API_KEY="your_livekit_api_key"
# LIVEKIT_API_SECRET="your_livekit_api_secret"
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY", "your_livekit_api_key")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET", "your_livekit_api_secret")

class LiveKitService:
    """
    Service for generating LiveKit access tokens for users to join a room/session.
    """
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or LIVEKIT_API_KEY
        self.api_secret = api_secret or LIVEKIT_API_SECRET

    def generate_token(
        self,
        identity: str,
        room: str,
        ttl_seconds: int = 3600,
        metadata: dict = None,
        permissions: dict = None,
    ) -> str:
        """
        Generate a JWT token for LiveKit room access.

        :param identity: Unique user ID for this session.
        :param room: Name of the room/session.
        :param ttl_seconds: How long the token is valid for (default 1 hour).
        :param metadata: Optional dict of metadata to embed.
        :param permissions: Optional dict of permissions (e.g., can_publish, can_subscribe).
        :return: JWT token as string.
        """
        now = int(time.time())
        payload = {
            "iss": self.api_key,
            "sub": identity,
            "aud": "livekit",
            "iat": now,
            "exp": now + ttl_seconds,
            "room": room,
            # Optional: Add permissions or metadata as needed
        }
        if metadata:
            payload["metadata"] = metadata
        if permissions:
            payload.update(permissions)

        token = jwt.encode(payload, self.api_secret, algorithm="HS256")
        # PyJWT >= 2.0 returns a str, <2.0 returns bytes
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        return token

# Example usage (for testing; remove/comment for production usage)
if __name__ == "__main__":
    service = LiveKitService()
    tok = service.generate_token(
        identity="user123",
        room="session_abc",
        permissions={"video": True, "audio": True}
    )
    print("LiveKit Token:", tok)