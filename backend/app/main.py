from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uuid
from app.game.manager import GameManager

app = FastAPI(title="Buzza Trivia API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game manager
game_manager = GameManager()

@app.get("/")
async def root():
    return {"message": "Buzza Backend is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_id = str(uuid.uuid4())
    
    try:
        # Wait for initial message with action (create_room or join_room)
        data = await websocket.receive_json()
        action = data.get("action")
        nickname = data.get("nickname")
        room_code = data.get("room_code")  # Only for join
        
        if action == "create_room":
            room_code = await game_manager.create_room(nickname, websocket, websocket_id)
            await websocket.send_json({
                "event": "room_created",
                "data": {"room_code": room_code, "is_host": True}
            })
            await game_manager.broadcast_player_list(room_code)
            
        elif action == "join_room":
            success = await game_manager.join_room(room_code, nickname, websocket, websocket_id)
            if success:
                await websocket.send_json({
                    "event": "room_joined",
                    "data": {"room_code": room_code, "is_host": False}
                })
                await game_manager.broadcast_player_list(room_code)
            else:
                await websocket.send_json({
                    "event": "error",
                    "data": {"message": "Failed to join room. Room might be full, game started, or nickname taken."}
                })
                await websocket.close()
                return
        
        # Keep connection alive and listen for messages
        while True:
            message = await websocket.receive_json()
            action = message.get("action")
            
            if action == "start_game":
                room_code = message.get("room_code")
                host_nickname = message.get("nickname")
                await game_manager.start_game(room_code, host_nickname)
                
            elif action == "submit_answer":
                room_code = message.get("room_code")
                nickname = message.get("nickname")
                answer = message.get("answer")
                await game_manager.submit_answer(room_code, nickname, answer)
                
            elif action == "leave_room":
                await game_manager.remove_player(websocket_id)
            
            # For debugging
            print(f"Received action: {action}")
            
    except WebSocketDisconnect:
        await game_manager.remove_player(websocket_id)