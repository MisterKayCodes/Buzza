import asyncio
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.game.manager import GameManager

async def test_game_manager():
    print("🧪 Testing Game Manager...")
    
    # Create manager instance
    manager = GameManager()
    
    # Test 1: Generate room code
    print("\n1. Testing room code generation...")
    code1 = manager.generate_room_code()
    code2 = manager.generate_room_code()
    print(f"   Code 1: {code1}")
    print(f"   Code 2: {code2}")
    assert len(code1) == 6, "Code should be 6 chars"
    assert code1 != code2, "Codes should be unique"
    print("   ✅ Room code generation works!")
    
    # Test 2: Create room (mock websocket)
    print("\n2. Testing room creation...")
    mock_ws = None  # We're just testing logic, not actual websocket
    room_code = await manager.create_room("TestHost", mock_ws, "ws_id_1")
    print(f"   Created room: {room_code}")
    
    assert room_code in manager.rooms, "Room should exist in manager"
    room = manager.rooms[room_code]
    assert room.host_nickname == "TestHost", "Host nickname wrong"
    assert len(room.players) == 1, "Should have 1 player"
    print("   ✅ Room creation works!")
    
    # Test 3: Join room
    print("\n3. Testing joining room...")
    joined = await manager.join_room(room_code, "Player2", mock_ws, "ws_id_2")
    assert joined == True, "Should join successfully"
    assert len(manager.rooms[room_code].players) == 2, "Should have 2 players"
    print("   ✅ Join room works!")
    
    # Test 4: Prevent duplicate nickname
    print("\n4. Testing duplicate nickname prevention...")
    joined = await manager.join_room(room_code, "TestHost", mock_ws, "ws_id_3")
    assert joined == False, "Should reject duplicate nickname"
    print("   ✅ Duplicate nickname blocked!")
    
    # Test 5: Get players list
    print("\n5. Testing get players list...")
    players = await manager.get_room_players(room_code)
    print(f"   Players: {players}")
    assert len(players) == 2, "Should return 2 players"
    assert players[0]["nickname"] == "TestHost" or players[1]["nickname"] == "TestHost"
    print("   ✅ Get players works!")
    
    print("\n" + "="*40)
    print("🎉 ALL TESTS PASSED! Game Manager basic functions work!")
    print("="*40)

if __name__ == "__main__":
    asyncio.run(test_game_manager())