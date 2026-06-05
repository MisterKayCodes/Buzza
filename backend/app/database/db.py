from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
import os

# Database file path (creates buzza.db in the backend folder)
DATABASE_URL = "sqlite+aiosqlite:///./buzza.db"

# Create engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()