import asyncio
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    
    # Test creating a room
    print("Testing room creation...")
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "action": "create_room",
            "nickname": "TestHost"
        }))
        response = await ws.recv()
        data = json.loads(response)
        print(f"Response: {data}")
        room_code = data["data"]["room_code"]
        
        # Should receive player list update
        response2 = await ws.recv()
        print(f"Player list: {json.loads(response2)}")
    
    print(f"\nRoom {room_code} created and host joined!")
    print("✅ WebSocket test passed!")

if __name__ == "__main__":
    asyncio.run(test_websocket())