from fastapi import status
from typing import Any


class DomainException(Exception):
    status_code: int = 400
    message: str | dict[str, Any] = "Ошибка бизнес-логики"

    def __init__(
        self,
        message: str | dict[str, Any] | None = None,
        status_code: int | None = None,
    ):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)


class UserNotFoundException(DomainException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Пользователь не найден"


class InvalidCredentialsException(DomainException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Неверный email или пароль"


class ValidationException(DomainException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    message = "Ошибка валидации данных"


class ConflictException(DomainException):
    status_code = status.HTTP_409_CONFLICT
    message = "conflict"


class FobbidenException(DomainException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Forbidden"


class UnauthorizedException(DomainException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized"
