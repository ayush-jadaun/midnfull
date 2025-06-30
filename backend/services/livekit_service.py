import os
import time
from datetime import timedelta
from livekit import api

class LiveKitService:
    def __init__(self):
        self.api_key = os.getenv("LIVEKIT_API_KEY")
        self.api_secret = os.getenv("LIVEKIT_API_SECRET")
        self.ws_url = os.getenv("LIVEKIT_WS_URL", "wss://mindfull-4wx7pfsc.livekit.cloud")
        
        if not self.api_key or not self.api_secret:
            raise ValueError(
                "LIVEKIT_API_KEY and LIVEKIT_API_SECRET environment variables must be set"
            )
        
        print(f"LiveKit initialized with API key: {self.api_key[:8]}...")

    def generate_token(
        self, 
        identity: str, 
        room: str, 
        can_publish_audio: bool = True,
        can_subscribe_audio: bool = True
    ) -> str:
        """
        Generate a LiveKit access token for a user to join a room.
        Grants permissions for audio publishing and subscribing.
        """
        try:
            token = api.AccessToken(self.api_key, self.api_secret)
            token = (token
                .with_identity(identity)
                .with_grants(api.VideoGrants(
                    room_join=True,
                    room=room,
                    can_publish=can_publish_audio,
                    can_subscribe=can_subscribe_audio,
                    can_publish_data=True,
                ))
                .with_ttl(timedelta(hours=1))  # Token valid for 1 hour
            )
            jwt_token = token.to_jwt()
            print(f"Generated audio token for user {identity} in room {room}")
            return jwt_token
        except Exception as e:
            print(f"Error generating LiveKit token: {str(e)}")
            raise Exception(f"Failed to generate LiveKit token: {str(e)}")

    def create_room(self, room_name: str) -> dict:
        """
        Create a new LiveKit room with audio call settings.
        Returns room details.
        """
        try:
            room_service = api.RoomService()
            room_service.api_key = self.api_key
            room_service.api_secret = self.api_secret
            
            room = room_service.create_room(
                api.CreateRoomRequest(
                    name=room_name,
                    empty_timeout=300,  # Room closes after 5 minutes of inactivity
                    max_participants=10,
                    metadata='{"type": "audio_call"}',
                )
            )
            return {
                "name": room.name,
                "sid": room.sid,
                "creation_time": room.creation_time,
            }
        except Exception as e:
            print(f"Error creating room: {str(e)}")
            raise Exception(f"Failed to create room: {str(e)}")

    def list_rooms(self) -> list:
        """
        Retrieve a list of currently active LiveKit rooms.
        """
        try:
            room_service = api.RoomService()
            room_service.api_key = self.api_key
            room_service.api_secret = self.api_secret
            
            rooms = room_service.list_rooms(api.ListRoomsRequest())
            return [
                {
                    "name": room.name,
                    "sid": room.sid,
                    "num_participants": room.num_participants,
                    "creation_time": room.creation_time,
                }
                for room in rooms.rooms
            ]
        except Exception as e:
            print(f"Error listing rooms: {str(e)}")
            raise Exception(f"Failed to list rooms: {str(e)}")

    def delete_room(self, room_name: str) -> bool:
        """
        Delete a LiveKit room by name.
        Returns True if successful, False otherwise.
        """
        try:
            room_service = api.RoomService()
            room_service.api_key = self.api_key
            room_service.api_secret = self.api_secret
            
            room_service.delete_room(
                api.DeleteRoomRequest(room=room_name)
            )
            print(f"Deleted room: {room_name}")
            return True
        except Exception as e:
            print(f"Error deleting room: {str(e)}")
            return False
