import os
import redis
from typing import List, Optional

# Example: REDIS_URL="redis://localhost:6379/0"
REDIS_URL = os.getenv("REDIS_URL", "redis://default:********@smiling-liger-48452.upstash.io:6379")

class RedisService:
    """
    Handles short-term memory operations (storing and retrieving recent messages) using Redis.
    Each session has a Redis list storing the last N messages.
    """
    def __init__(self, url: Optional[str] = None, max_messages: int = 10):
        self.url = url or REDIS_URL
        self.max_messages = max_messages
        self.redis = redis.Redis.from_url(self.url, decode_responses=True)

    def get_history_key(self, session_id: str) -> str:
        """Returns the Redis key for a session's message history."""
        return f"session:{session_id}:history"

    def add_message(self, session_id: str, message: str) -> None:
        """
        Adds a message to the session's message list.
        Maintains only the most recent `max_messages` messages.
        """
        key = self.get_history_key(session_id)
        # Add message to the right (acts as a queue)
        self.redis.rpush(key, message)
        # Trim list to last N messages
        self.redis.ltrim(key, -self.max_messages, -1)

    def get_recent_messages(self, session_id: str) -> List[str]:
        """
        Retrieves the most recent messages for a session.
        Returns a list of strings, or an empty list if none exist.
        """
        key = self.get_history_key(session_id)
        return self.redis.lrange(key, 0, -1)

    def clear_history(self, session_id: str) -> None:
        """
        Deletes the message history for a session.
        """
        key = self.get_history_key(session_id)
        self.redis.delete(key)

# Example usage (to be removed/commented in production modules):
if __name__ == "__main__":
    # For quick testing. Set REDIS_URL as needed.
    service = RedisService()
    test_session = "12345"
    service.add_message(test_session, "Hello, this is a test message.")
    print(service.get_recent_messages(test_session))
    service.clear_history(test_session)