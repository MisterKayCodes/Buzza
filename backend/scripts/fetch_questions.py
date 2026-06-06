import asyncio
import httpx
import sys
import os
import html

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.db import AsyncSessionLocal, engine, Base
from app.database.models import Question

async def create_tables():
    """Create tables if they don't exist"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables ready")

async def fetch_opentdb():
    questions_to_add = []
    
    async with httpx.AsyncClient() as client:
        for difficulty in ["easy", "medium"]:
            url = f"https://opentdb.com/api.php?amount=50&difficulty={difficulty}&type=multiple"
            print(f"Fetching from: {url}")
            
            response = await client.get(url)
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 429:
                print("Rate limited! Waiting 10 seconds...")
                await asyncio.sleep(10)
                response = await client.get(url)
            
            data = response.json()
            
            if data.get("response_code") != 0:
                print(f"Error: {data}")
                continue
            
            for item in data["results"]:
                clean_question = html.unescape(item["question"])
                clean_answer = html.unescape(item["correct_answer"])
                
                q = Question(
                    question_text=clean_question,
                    question_type="factual",
                    correct_answer=clean_answer,
                    alternative_answers=None,
                    difficulty=difficulty,
                    category=item["category"],
                    source="opentdb"
                )
                questions_to_add.append(q)
            
            print(f"Added {len(data['results'])} questions from {difficulty}")
            
            # Wait 6 seconds before next request (respect rate limit)
            await asyncio.sleep(6)
    
    if questions_to_add:
        async with AsyncSessionLocal() as session:
            session.add_all(questions_to_add)
            await session.commit()
        print(f"✅ Added {len(questions_to_add)} total questions to database")
    else:
        print("❌ No questions were fetched")

async def main():
    await create_tables()
    await fetch_opentdb()

if __name__ == "__main__":
    asyncio.run(main())