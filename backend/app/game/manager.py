import asyncio
import random
import string
from typing import Dict, Optional, Set
from fastapi import WebSocket

from app.game.models import RoomState, Player, GameState

class GameManager:
    def __init__(self):
        self.rooms: Dict[str, RoomState] = {}  # room_code -> RoomState
        self.player_connections: Dict[str, WebSocket] = {}  # websocket_id -> WebSocket
        self.room_lock = asyncio.Lock()
    
    def generate_room_code(self) -> str:
        """Generate a 6-character alphanumeric room code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if code not in self.rooms:
                return code
    
    async def create_room(self, nickname: str, websocket: WebSocket, websocket_id: str) -> str:
        """Create a new room with the player as host"""
        room_code = self.generate_room_code()
        
        async with self.room_lock:
            # Create player
            player = Player(
                nickname=nickname,
                websocket_id=websocket_id,
                is_host=True,
                room_code=room_code
            )
            
            # Create room
            room = RoomState(
                room_code=room_code,
                host_nickname=nickname,
                players={websocket_id: player},
                scores={nickname: 0}
            )
            
            self.rooms[room_code] = room
            self.player_connections[websocket_id] = websocket
            
            return room_code
    
    async def join_room(self, room_code: str, nickname: str, websocket: WebSocket, websocket_id: str) -> bool:
        """Join an existing room"""
        async with self.room_lock:
            if room_code not in self.rooms:
                return False
            
            room = self.rooms[room_code]
            
            # Check if game already started
            if room.game_state != GameState.LOBBY:
                return False
            
            # Check for duplicate nickname
            for player in room.players.values():
                if player.nickname.lower() == nickname.lower():
                    return False
            
            # Create player
            player = Player(
                nickname=nickname,
                websocket_id=websocket_id,
                is_host=False,
                room_code=room_code
            )
            
            room.players[websocket_id] = player
            room.scores[nickname] = 0
            self.player_connections[websocket_id] = websocket
            
            return True
    
    async def get_room_players(self, room_code: str) -> list:
        """Get list of players in a room"""
        if room_code not in self.rooms:
            return []
        
        room = self.rooms[room_code]
        return [
            {
                "nickname": p.nickname,
                "score": p.score,
                "is_host": p.is_host
            }
            for p in room.players.values()
        ]