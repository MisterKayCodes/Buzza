import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.db import AsyncSessionLocal
from app.database.models import Question

async def add_questions():
    questions_to_add = []
    
    # List-style questions (10)
    list_questions = [
        ("Name a country in Africa that starts with the letter 'N'", "list", "Nigeria", '["Nigeria","Niger","Namibia"]', "medium", "Geography"),
        ("Name a color that starts with 'B'", "list", "Blue", '["Blue","Black","Brown","Beige","Bronze","Burgundy"]', "easy", "General"),
        ("Name a fruit that starts with the letter 'A'", "list", "Apple", '["Apple","Apricot","Avocado","Açaí Berry","Atemoya","Acerola cherry","Amla"]', "easy", "Food"),
        ("Name any African country that has 7 letters in its name", "list", "Algeria", '["Algeria","Morocco","Nigeria","Somalia","Tunisia","Burundi","Eritrea","Namibia","Comoros","Lesotho"]', "medium", "Geography"),
        ("Name a day of the week that starts with 'T'", "list", "Tuesday", '["Tuesday","Thursday"]', "easy", "General"),
        ("Name a month with exactly 30 days", "list", "April", '["April","June","September","November"]', "medium", "General"),
        ("Name a Nigerian state that starts with the letter 'Y'", "list", "Yobe", '["Yobe"]', "easy", "Nigerian"),
        ("Name a sport played with a ball", "list", "Football", '["Football","Basketball","Tennis","Volleyball","Baseball","Rugby","Golf","Cricket","Handball","Table tennis"]', "easy", "Sports"),
        ("Name a European country that starts with 'G'", "list", "Germany", '["Germany","Greece","Georgia"]', "medium", "Geography"),
        ("Name an Asian country that starts with 'J'", "list", "Japan", '["Japan","Jordan"]', "medium", "Geography"),
    ]
    
    for q in list_questions:
        questions_to_add.append(Question(
            question_text=q[0],
            question_type=q[1],
            correct_answer=q[2],
            alternative_answers=q[3],
            difficulty=q[4],
            category=q[5],
            source="manual"
        ))
    
    # True/False questions (5 easy, 5 medium)
    tf_questions = [
        ("The sun rises in the west", "truefalse", "False", None, "easy", "General"),
        ("Water boils at 100 degrees Celsius at sea level", "truefalse", "True", None, "easy", "Science"),
        ("Lagos is the capital city of Nigeria", "truefalse", "False", None, "easy", "Nigerian"),
        ("Humans have 4 chambers in their heart", "truefalse", "True", None, "easy", "Science"),
        ("Bananas grow on trees", "truefalse", "False", None, "easy", "Food"),
        ("Nigeria has 36 states including the FCT", "truefalse", "True", None, "medium", "Nigerian"),
        ("The fastest land animal is the lion", "truefalse", "False", None, "medium", "Animals"),
        ("The Great Wall of China is visible from space", "truefalse", "False", None, "medium", "Geography"),
        ("The first computer was invented in the 21st century", "truefalse", "False", None, "medium", "Science"),
        ("Sharks are mammals", "truefalse", "False", None, "medium", "Animals"),
    ]
    
    for q in tf_questions:
        questions_to_add.append(Question(
            question_text=q[0],
            question_type=q[1],
            correct_answer=q[2],
            alternative_answers=q[3],
            difficulty=q[4],
            category=q[5],
            source="manual"
        ))
    
    # Fill-in-the-blank questions
    fill_questions = [
        ("The capital of Nigeria is ______", "fillblank", "Abuja", None, "easy", "Nigerian"),
        ("The largest ocean on Earth is the ______ Ocean", "fillblank", "Pacific", None, "easy", "Geography"),
        ("The fastest land animal is the ______", "fillblank", "Cheetah", None, "easy", "Animals"),
        ("The longest river in Africa is the River ______", "fillblank", "Nile", None, "medium", "Geography"),
        ("The planet known as the Red Planet is ______", "fillblank", "Mars", None, "easy", "Science"),
        ("The author of 'Things Fall Apart' is Chinua ______", "fillblank", "Achebe", None, "medium", "Nigerian"),
        ("The first president of Nigeria was Nnamdi ______", "fillblank", "Azikiwe", None, "medium", "Nigerian"),
        ("The chemical symbol for water is ______", "fillblank", "H2O", None, "easy", "Science"),
        ("The tallest mountain in the world is Mount ______", "fillblank", "Everest", None, "easy", "Geography"),
        ("The currency of Nigeria is the Nigerian ______", "fillblank", "Naira", None, "easy", "Nigerian"),
    ]
    
    for q in fill_questions:
        questions_to_add.append(Question(
            question_text=q[0],
            question_type=q[1],
            correct_answer=q[2],
            alternative_answers=q[3],
            difficulty=q[4],
            category=q[5],
            source="manual"
        ))
    
    # Save to database
    async with AsyncSessionLocal() as session:
        session.add_all(questions_to_add)
        await session.commit()
    
    print(f"✅ Added {len(questions_to_add)} new questions")
    print(f"   - List-style: 10")
    print(f"   - True/False: 10")
    print(f"   - Fill-blank: 10")
    print(f"   Total questions now: ~130")

if __name__ == "__main__":
    asyncio.run(add_questions())