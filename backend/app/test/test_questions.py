import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.game.questions import get_random_questions

async def test_get_questions():
    print("Testing question fetching...")
    
    # Get 20 random questions
    questions = await get_random_questions(20)
    
    print(f"✅ Got {len(questions)} questions")
    
    # Show first 3 questions as sample
    print("\nSample questions:")
    for i, q in enumerate(questions[:3]):
        print(f"\n{i+1}. {q['question_text']}")
        print(f"   Type: {q['question_type']}")
        print(f"   Difficulty: {q['difficulty']}")
        print(f"   Correct answer: {q['correct_answer']}")
        if q['alternative_answers']:
            print(f"   Also accepts: {q['alternative_answers']}")
    
    # Show type breakdown
    types = {}
    for q in questions:
        t = q['question_type']
        types[t] = types.get(t, 0) + 1
    
    print(f"\n📊 Question type breakdown:")
    for t, count in types.items():
        print(f"   {t}: {count}")

if __name__ == "__main__":
    asyncio.run(test_get_questions())