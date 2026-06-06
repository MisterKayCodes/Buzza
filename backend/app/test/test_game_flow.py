import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.game.manager import GameManager

async def test_game_flow():
    print("🧪 Testing Game Flow...")
    
    manager = GameManager()
    
    # Create a room
    room_code = await manager.create_room("HostPlayer", None, "ws_1")
    print(f"✅ Room created: {room_code}")
    
    # Join with second player
    await manager.join_room(room_code, "Player2", None, "ws_2")
    print("✅ Player2 joined")
    
    # Check players
    players = await manager.get_room_players(room_code)
    print(f"✅ Players in room: {[p['nickname'] for p in players]}")
    
    # Start game
    result = await manager.start_game(room_code, "HostPlayer")
    if result:
        print("✅ Game started!")
    else:
        print("❌ Failed to start game")
    
    # Check room state
    room = manager.rooms[room_code]
    print(f"✅ Game state: {room.game_state}")
    print(f"✅ Questions loaded: {len(room.questions)}")
    
    # Test answer submission
    if room.questions:
        first_question = room.questions[0]
        print(f"\n📝 First question: {first_question['question_text']}")
        print(f"   Correct answer: {first_question['correct_answer']}")
        
        # Submit correct answer
        result = await manager.submit_answer(room_code, "Player2", first_question['correct_answer'])
        print(f"✅ Submit answer result: {result}")
        
        # Check scores
        print(f"✅ Scores: {room.scores}")

if __name__ == "__main__":
    asyncio.run(test_game_flow())