import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

# load .env (if present)
load_dotenv(dotenv_path=".env", encoding="utf-8")

# read DATABASE_URL (case-insensitive)
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("database_url") or os.getenv("DbUrl")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not found in environment or .env file. Please set it before running.")

# create async engine and session factory
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Base for models
Base = declarative_base()

# FastAPI / route dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
