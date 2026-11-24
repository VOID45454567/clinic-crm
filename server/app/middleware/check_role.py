from app.security import oauth_scheme
from fastapi import Depends
from app.services.auth_service import AuthService
from app.db.models.user import UserPublic
from app.http.exceptions.domain import ForbiddenException


class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self, token: str = Depends(oauth_scheme), auth_service: AuthService = Depends()
    ) -> UserPublic:
        user = await auth_service.extract_user(token)

        if user.role not in self.allowed_roles:
            raise ForbiddenException("Недостаточно прав для этого действия")

        return user
