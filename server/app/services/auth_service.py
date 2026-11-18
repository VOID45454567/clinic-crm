from app.db.models.User import UserPublic
from app.http.responses.auth.login_response import LoginResponse
import jwt
from datetime import timedelta
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.security.oauth2 import OAuth2PasswordBearer

from app.db.connect import get_session
from app.http.exceptions.domain import (
    FobbidenException,
    UnauthorizedException,
    InvalidCredentialsException,
)

from app.services.user_service import find_user_by_id, find_user_by_email
from app.services.jwt_service import decode_token, create_token
from app.conf.config import settings
from app.security import verify_password
from app.db.models import User

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class AuthService:
    def __init__(self, db: AsyncSession = Depends(get_session)):
        self.db = db

    async def login(self, email: str, password: str) -> LoginResponse:
        user = await find_user_by_email(email, self.db)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        return self.generate_tokens_pair(user)

    async def extract_user(self, token: str):
        try:
            payload = decode_token(token)
        except jwt.PyJWTError:
            raise UnauthorizedException("Невалидный токен")

        user_id = payload.get("sub")
        if (user_id is None) or (payload.get("type") != "access"):
            raise UnauthorizedException("Невалидный токен")

        user = await find_user_by_id(int(user_id), self.db)
        if not user:
            raise UnauthorizedException("Пользователь не найден")
        return user

    def generate_tokens_pair(self, user: UserPublic) -> LoginResponse:
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
