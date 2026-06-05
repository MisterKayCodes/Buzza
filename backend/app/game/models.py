from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class GameState(str, Enum):
    LOBBY = "lobby"
    PLAYING = "playing"
    RESULTS = "results"

class Player(BaseModel):
    nickname: str
    websocket_id: str
    score: int = 0
    is_host: bool = False
    room_code: str

class RoomState(BaseModel):
    room_code: str
    host_nickname: str
    players: Dict[str, Player] = {}  # key: websocket_id
    game_state: GameState = GameState.LOBBY
    current_question_index: int = 0
    questions: List[Dict[str, Any]] = []
    scores: Dict[str, int] = {}  # key: nickname, value: score
    timer_task: Optional[Any] = None
    question_locked: bool = False