from typing import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, \
    async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

load_dotenv()

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_db() -> AsyncSession:
    """Create a new database session for each request."""
    db = async_session_maker()
    try:
        yield db
    finally:
        await db.close()