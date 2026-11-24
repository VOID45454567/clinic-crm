from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.connect import get_session
from app.db.models.user import User, UserCreate, UserUpdate
from app.http.exceptions.domain import (
    ConflictException,
    UserNotFoundException,
)
from app.security import hash_password


class UserService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_session),
    ):
        self.db = db

    async def find_user_by_email(self, email: str) -> User | None:

        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def find_user_by_id(self, id: int) -> User | None:
        return await self.db.get(User, id)

    async def create_user(self, dto: UserCreate):
        existing_user = await self.find_user_by_email(dto.email)
        if existing_user:
            raise ConflictException("Пользователь с таким email уже существует")

        new_user = User(
            email=dto.email,
            is_active=True,
            hashed_password=hash_password(dto.password),
            role=dto.role,
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        return new_user

    async def update_user(self, dto: UserUpdate, user_id: int):

        user = await self.db.get(User, user_id)
        if not user:
            raise UserNotFoundException()

        update_data = dto.model_dump(exclude_unset=True)

        if "email" in update_data and update_data["email"] != user.email:
            statement = select(User).where(User.email == update_data["email"])
            result = await self.db.execute(statement)
            if result.scalars().first():
                raise ConflictException("Пользователь с таким email уже существует")

        if "password" in update_data:
            plain_password = update_data.pop("password")
            update_data["hashed_password"] = hash_password(plain_password)

        for key, value in update_data.items():
            setattr(user, key, value)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user
