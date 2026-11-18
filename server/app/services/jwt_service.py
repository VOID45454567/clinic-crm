from app.security import ALGORITHM
import jwt
from app.conf.config import settings
from datetime import timezone
from datetime import datetime
from typing import Any
from typing import Literal
from datetime import timedelta


def create_token(
    subject: str,
    expires_delta: timedelta,
    token_type: Literal["access", "refresh"] = "access",
    extra_data: dict[str, Any] | None = None,
) -> str:

    now = datetime.now(timezone.utc)
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
