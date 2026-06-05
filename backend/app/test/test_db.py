import asyncio
import sys
from pathlib import Path

# Add the backend folder to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.database.db import engine, Base
from app.database.models import NigerianQuestion, Room, GameSession, Player
from app.database.db import AsyncSessionLocal

async def init_db():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Database tables created successfully!")

async def test_insert():
    async with AsyncSessionLocal() as session:
        # Insert a test Nigerian question
        test_q = NigerianQuestion(
            question="What is the capital of Nigeria?",
            correct_answer="Abuja",
            alternative_answers='["Abuja FCT", "Abuja City"]',
            category="Geography",
            difficulty="easy"
        )
        session.add(test_q)
        await session.commit()
        print("✅ Test question inserted!")
        print("✅ Database test complete!")

async def main():
    await init_db()
    await test_insert()

if __name__ == "__main__":
    asyncio.run(main())