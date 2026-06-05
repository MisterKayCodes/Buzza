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

    # --- NEWLY ADDED METHODS BELOW ---

    async def broadcast_to_room(self, room_code: str, event: str, data: dict):
        """Send event to all players in a room"""
        if room_code not in self.rooms:
            return
            
        room = self.rooms[room_code]
        message = {"event": event, "data": data}
        
        for ws_id, player in room.players.items():
            if ws_id in self.player_connections:
                websocket = self.player_connections[ws_id]
                try:
                    await websocket.send_json(message)
                except Exception:
                    # Player disconnected, ignore and move on
                    pass

    async def broadcast_player_list(self, room_code: str):
        """Broadcast updated player list to room"""
        players = await self.get_room_players(room_code)
        await self.broadcast_to_room(room_code, "player_list_update", {"players": players})

    async def remove_player(self, websocket_id: str):
        """Remove a disconnected player"""
        # Find which room they were in
        room_code = None
        for code, room in self.rooms.items():
            if websocket_id in room.players:
                room_code = code
                break
            
        if room_code:
            async with self.room_lock:
                room = self.rooms[room_code]
                player = room.players.get(websocket_id)
                
                if player:
                    nickname = player.nickname
                    was_host = player.is_host
                    
                    # Remove player
                    del room.players[websocket_id]
                    if nickname in room.scores:
                        del room.scores[nickname]
                    
                    # Remove websocket connection
                    if websocket_id in self.player_connections:
                        del self.player_connections[websocket_id]
                    
                    # If room is empty, delete it completely
                    if len(room.players) == 0:
                        del self.rooms[room_code]
                        return
                    
                    # If host left, assign a new host dynamically
                    if was_host and len(room.players) > 0:
                        new_host_id = list(room.players.keys())[0]
                        room.players[new_host_id].is_host = True
                        room.host_nickname = room.players[new_host_id].nickname
                    
                    # Broadcast updated player list
                    await self.broadcast_player_list(room_code)
                    
                    # Broadcast leave message
                    await self.broadcast_to_room(room_code, "player_left", {"nickname": nickname})