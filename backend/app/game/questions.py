import random
from sqlalchemy import select, func
from app.database.db import AsyncSessionLocal
from app.database.models import Question

async def get_random_questions(limit: int = 20) -> list:
    """
    Fetch random questions from the database.
    Returns a list of question dictionaries ready for gameplay.
    """
    async with AsyncSessionLocal() as session:
        # Get random questions from database
        result = await session.execute(
            select(Question).order_by(func.random()).limit(limit)
        )
        questions = result.scalars().all()
        
        # Convert to list of dictionaries
        questions_list = []
        for q in questions:
            questions_list.append({
                "id": q.id,
                "question_text": q.question_text,
                "question_type": q.question_type,
                "correct_answer": q.correct_answer,
                "alternative_answers": q.alternative_answers,
                "difficulty": q.difficulty,
                "category": q.category
            })
        
        return questions_list