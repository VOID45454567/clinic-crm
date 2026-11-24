from datetime import timedelta

import jwt
from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.conf.config import settings
from app.db.connect import get_session
from app.db.models.user import User
from app.http.exceptions.domain import (
    InvalidCredentialsException,
    UnauthorizedException,
)
from app.http.responses.auth.login_response import LoginResponse
from app.security import verify_password
from app.services.jwt_service import create_token, decode_token


class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def find_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = await self.db.execute(statement)
        return result.scalars().first()

    async def find_user_by_id(self, user_id: int) -> User | None:
        return await self.db.get(User, user_id)

    async def login(self, email: str, password: str) -> LoginResponse:
        user = await self.find_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        return self.generate_tokens_pair(user)

    async def extract_user(self, token: str) -> User:
        try:
            payload = decode_token(token)
        except jwt.PyJWTError:
            raise UnauthorizedException("Невалидный токен") from None

        user_id = payload.get("sub")
        if (user_id is None) or (payload.get("type") != "access"):
            raise UnauthorizedException("Невалидный токен")

        user = await self.find_user_by_id(int(user_id))
        if not user:
            raise UnauthorizedException("Пользователь не найден")
        return user

    async def refresh_tokens(self, refresh_token: str) -> LoginResponse:
        try:
            payload = decode_token(refresh_token)
        except jwt.PyJWTError:
            raise UnauthorizedException("Невалидный refresh token") from None

        user_id = payload.get("sub")
        if (user_id is None) or (payload.get("type") != "refresh"):
            raise UnauthorizedException("Невалидный refresh token")

        user = await self.find_user_by_id(int(user_id))
        if not user:
            raise UnauthorizedException("Пользователь не найден")

        return self.generate_tokens_pair(user)

    def generate_tokens_pair(self, user: User) -> LoginResponse:
        access_token = create_token(
            str(user.id),
            timedelta(minutes=settings.ACCESS_TOKEN_TTL_MIN),
            "access",
            {"role": user.role},
        )
        refresh_token = create_token(
            str(user.id),
            timedelta(days=settings.REFRESH_TOKEN_TTL_DAYS),
            "refresh",
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )
