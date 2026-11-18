from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.models.user import User


async def find_user_by_email(email: str, db: AsyncSession) -> User | None:
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalars().first()


async def find_user_by_id(id: int, db: AsyncSession) -> User | None:
    return await db.get(User, id)
