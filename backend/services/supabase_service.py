import os
import psycopg2
import numpy as np
from typing import List, Optional, Tuple, Dict, Any

# Example environment variable for PostgreSQL connection
# POSTGRES_URL="postgresql://user:password@host:port/dbname"
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/mydb")

# Table and schema details (you must create this table in your db)
# Example table schema for long-term memory with pgvector:
# CREATE EXTENSION IF NOT EXISTS vector;
# CREATE TABLE IF NOT EXISTS conversation_memory (
#     id SERIAL PRIMARY KEY,
#     session_id TEXT,
#     summary TEXT,
#     embedding VECTOR(1536), -- size depends on your embedding model
#     created_at TIMESTAMP DEFAULT NOW()
# );
VECTOR_DIM = 1536  # Replace with your embedding model's dimension

class SupabaseService:
    """
    Handles long-term memory: storing conversation summaries & embeddings,
    and retrieving most similar memories using pgvector and cosine similarity.
    """
    def __init__(self, db_url: Optional[str] = None):
        self.db_url = db_url or POSTGRES_URL
        self.conn = psycopg2.connect(self.db_url)
        self.conn.autocommit = True

    def store_memory(self, session_id: str, summary: str, embedding: List[float]) -> None:
        """
        Stores a conversation summary and its embedding vector for a session.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversation_memory (session_id, summary, embedding)
                VALUES (%s, %s, %s)
                """,
                (session_id, summary, embedding)
            )

    def retrieve_similar_memories(
        self, query_embedding: List[float], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieves the top_k most similar conversation memories using cosine similarity.
        Returns list of dicts with summary and similarity score.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT id, session_id, summary,
                    (embedding <#> %s::vector) AS cosine_distance
                FROM conversation_memory
                ORDER BY cosine_distance ASC
                LIMIT %s
                """,
                (query_embedding, top_k)
            )
            rows = cur.fetchall()
        # Prepare result as list of dicts
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "session_id": row[1],
                "summary": row[2],
                "similarity": 1 - row[3],  # cosine_distance: lower is more similar
            })
        return result

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()

# Example usage (for quick dev test; remove/comment out in production)
if __name__ == "__main__":
    service = SupabaseService()
    test_session = "test_123"
    fake_embedding = np.random.rand(VECTOR_DIM).astype(np.float32).tolist()
    service.store_memory(test_session, "Sample summary for testing.", fake_embedding)
    similar = service.retrieve_similar_memories(fake_embedding, top_k=2)
    print(similar)
    service.close()