from contextlib import asynccontextmanager

from configs.core import settings
from database import Base
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

if "asyncpg" in settings.SQL_URI:
    engine = create_async_engine(settings.SQL_URI)
    SessionLocal = async_sessionmaker(autoflush=False, bind=engine)

    async def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            await db.close()

    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await init_db()
        yield

else:
    engine = create_engine(settings.SQL_URI, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def init_db():
        Base.metadata.create_all(engine)

    def lifespan(app: FastAPI):
        init_db()
        yield
