from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt

from app.conf.config import settings
from app.security import ALGORITHM


def create_token(
    subject: str,
    expires_delta: timedelta,
    token_type: Literal["access", "refresh"] = "access",
    extra_data: dict[str, Any] | None = None,
) -> str:

    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
        **(extra_data or {}),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:

    return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
