from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean
from sqlalchemy.sql import func
from app.database.db import Base

class NigerianQuestion(Base):
    __tablename__ = "nigerian_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    correct_answer = Column(String(200), nullable=False)
    alternative_answers = Column(JSON, nullable=True)  # JSON array like ["Abuja", "Abuja FCT"]
    category = Column(String(100), nullable=False)
    difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<NigerianQuestion(id={self.id}, question='{self.question[:50]}...', difficulty='{self.difficulty}')>"


class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String(6), unique=True, index=True, nullable=False)
    host_nickname = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    max_players = Column(Integer, default=10)
    current_players = Column(Integer, default=0)
    game_state = Column(String(20), default="lobby")  # lobby, playing, ended
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Room(room_code='{self.room_code}', state='{self.game_state}', players={self.current_players})>"


class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    room_code = Column(String(6), nullable=False)
    questions_used = Column(Text, nullable=False)  # JSON string of question IDs and text
    scores = Column(Text, nullable=False)  # JSON string of {nickname: score}
    winner = Column(String(50), nullable=True)
    total_questions = Column(Integer, default=20)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)



class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), nullable=False)
    room_code = Column(String(6), nullable=False)
    score = Column(Integer, default=0)
    is_host = Column(Boolean, default=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    left_at = Column(DateTime(timezone=True), nullable=True)


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String(500), nullable=False)
    question_type = Column(String(20), nullable=False)  # factual, list, truefalse, fillblank
    correct_answer = Column(String(200), nullable=True)  # for factual/truefalse/fillblank
    alternative_answers = Column(JSON, nullable=True)  # for list questions
    difficulty = Column(String(10), nullable=False)  # easy, medium
    category = Column(String(50), nullable=True)
    source = Column(String(20), default="opentdb")  # opentdb or nigerian