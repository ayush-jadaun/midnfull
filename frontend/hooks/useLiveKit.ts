import { useState, useCallback } from "react";


export function useLiveKit() {
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const BACKEND_URL="http://localhost:8000"

  const getToken = useCallback(async (roomId: string, userId: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `${BACKEND_URL}/livekit/token/${roomId}?user_id=${userId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get LiveKit token");
      }

      const data = await response.json();
      setToken(data.token);
      return data.token;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    token,
    error,
    isLoading,
    getToken,
  };
}
