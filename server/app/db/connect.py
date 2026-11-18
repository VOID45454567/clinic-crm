from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.conf.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session():
    async with SessionLocal() as session:
        yield session
