import asyncio
import random
import string
from typing import Dict, Optional, Set
from fastapi import WebSocket

from app.game.models import RoomState, Player, GameState
from app.game.questions import get_random_questions

class GameManager:
    def __init__(self):
        self.rooms: Dict[str, RoomState] = {}
        self.player_connections: Dict[str, WebSocket] = {}
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
            player = Player(
                nickname=nickname,
                websocket_id=websocket_id,
                is_host=True,
                room_code=room_code
            )
            
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
            
            if room.game_state != GameState.LOBBY:
                return False
            
            for player in room.players.values():
                if player.nickname.lower() == nickname.lower():
                    return False
            
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
                    pass

    async def broadcast_player_list(self, room_code: str):
        """Broadcast updated player list to room"""
        players = await self.get_room_players(room_code)
        await self.broadcast_to_room(room_code, "player_list_update", {"players": players})

    async def remove_player(self, websocket_id: str):
        """Remove a disconnected player"""
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
                    
                    del room.players[websocket_id]
                    if nickname in room.scores:
                        del room.scores[nickname]
                    
                    if websocket_id in self.player_connections:
                        del self.player_connections[websocket_id]
                    
                    if len(room.players) == 0:
                        del self.rooms[room_code]
                        return
                    
                    if was_host and len(room.players) > 0:
                        new_host_id = list(room.players.keys())[0]
                        room.players[new_host_id].is_host = True
                        room.host_nickname = room.players[new_host_id].nickname
                    
                    await self.broadcast_player_list(room_code)
                    await self.broadcast_to_room(room_code, "player_left", {"nickname": nickname})

    async def start_game(self, room_code: str, host_nickname: str) -> bool:
        """Start the game in a room (host only)"""
        async with self.room_lock:
            if room_code not in self.rooms:
                return False
            
            room = self.rooms[room_code]
            
            if room.host_nickname != host_nickname:
                return False
            
            if room.game_state != GameState.LOBBY:
                return False
            
            if len(room.players) < 2:
                await self.broadcast_to_room(room_code, "error", {"message": "Need at least 2 players to start"})
                return False
            
            questions = await get_random_questions(20)
            
            if len(questions) < 20:
                await self.broadcast_to_room(room_code, "error", {"message": "Not enough questions available"})
                return False
            
            room.questions = questions
            room.current_question_index = 0
            room.game_state = GameState.PLAYING
            
            await self.broadcast_to_room(room_code, "game_started", {
                "total_questions": 20
            })
            
            await self.send_current_question(room_code)
            
            return True

    async def send_current_question(self, room_code: str):
        """Send the current question to all players in the room"""
        if room_code not in self.rooms:
            return
        
        room = self.rooms[room_code]
        
        if room.current_question_index >= len(room.questions):
            await self.end_game(room_code)
            return
        
        current_q = room.questions[room.current_question_index]
        
        question_data = {
            "question_number": room.current_question_index + 1,
            "total_questions": len(room.questions),
            "question_text": current_q["question_text"],
            "question_type": current_q["question_type"],
            "timer_seconds": 15
        }
        
        await self.broadcast_to_room(room_code, "question_show", question_data)
        
        room.question_locked = False
        
        # Cancel existing timer if any
        if room.timer_task:
            room.timer_task.cancel()
        
        # Start new timer and store it
        room.timer_task = asyncio.create_task(self.start_question_timer(room_code))

    async def start_question_timer(self, room_code: str):
        """Start 15 second timer for current question"""
        await asyncio.sleep(15)
        
        if room_code in self.rooms:
            room = self.rooms[room_code]
            
            # Clear the stored timer reference
            room.timer_task = None
            
            if not room.question_locked:
                room.question_locked = True
                
                current_q = room.questions[room.current_question_index]
                
                await self.broadcast_to_room(room_code, "timeout", {
                    "correct_answer": current_q["correct_answer"],
                    "message": "Time's up! No one got it right."
                })
                
                await asyncio.sleep(2)
                await self.next_question(room_code)

    async def next_question(self, room_code: str):
        """Move to next question or end game"""
        if room_code not in self.rooms:
            return
        
        room = self.rooms[room_code]
        
        room.current_question_index += 1
        
        if room.current_question_index >= len(room.questions):
            await self.end_game(room_code)
        else:
            await self.send_current_question(room_code)

    async def end_game(self, room_code: str):
        """End the game and show final results"""
        if room_code not in self.rooms:
            return
        
        room = self.rooms[room_code]
        room.game_state = GameState.RESULTS
        
        leaderboard = []
        for nickname, score in room.scores.items():
            leaderboard.append({"nickname": nickname, "score": score})
        
        leaderboard.sort(key=lambda x: x["score"], reverse=True)
        
        await self.broadcast_to_room(room_code, "game_over", {
            "leaderboard": leaderboard,
            "winner": leaderboard[0]["nickname"] if leaderboard else None
        })

    async def submit_answer(self, room_code: str, nickname: str, answer: str) -> bool:
        """Submit an answer for a question"""
        import json
        
        if room_code not in self.rooms:
            return False
        
        room = self.rooms[room_code]
        
        if room.game_state != GameState.PLAYING:
            return False
        
        if room.question_locked:
            await self.broadcast_to_room(room_code, "answer_result", {
                "nickname": nickname,
                "correct": False,
                "message": "Too late! Someone already answered correctly."
            })
            return False
        
        current_q = room.questions[room.current_question_index]
        correct_answer = current_q["correct_answer"].strip().lower()
        user_answer = answer.strip().lower()
        
        is_correct = user_answer == correct_answer
        
        if not is_correct and current_q["alternative_answers"]:
            alternatives = json.loads(current_q["alternative_answers"])
            for alt in alternatives:
                if user_answer == alt.strip().lower():
                    is_correct = True
                    break
        
        if is_correct:
            # Cancel the timer
            if room.timer_task:
                room.timer_task.cancel()
                room.timer_task = None
            
            room.question_locked = True
            
            room.scores[nickname] = room.scores.get(nickname, 0) + 1
            
            for player in room.players.values():
                if player.nickname == nickname:
                    player.score = room.scores[nickname]
                    break
            
            await self.broadcast_to_room(room_code, "answer_correct", {
                "nickname": nickname,
                "points_awarded": 1,
                "new_score": room.scores[nickname],
                "correct_answer": current_q["correct_answer"]
            })
            
            asyncio.create_task(self.delay_and_next(room_code))
            
            return True
        else:
            # Broadcast to everyone that someone attempted but failed
            await self.broadcast_to_room(room_code, "answer_wrong_attempt", {
                "nickname": nickname,
                "message": f"{nickname} attempted but failed!"
            })
            
            # Send specific feedback to the player who answered wrong
            for ws_id, player in room.players.items():
                if player.nickname == nickname:
                    websocket = self.player_connections.get(ws_id)
                    if websocket:
                        await websocket.send_json({
                            "event": "answer_wrong",
                            "data": {
                                "message": "Wrong answer! Try again."
                            }
                        })
                    break
            
            return False

    async def delay_and_next(self, room_code: str):
        """Delay 2 seconds then move to next question"""
        await asyncio.sleep(2)
        await self.next_question(room_code)