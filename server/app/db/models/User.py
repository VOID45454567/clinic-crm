from typing import Literal
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    role: str = Field(default="registrar")
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserCreate(UserBase):
    role: Literal["admin", "doctor", "registrar"] = "registrar"
    password: str


class UserUpdate(SQLModel):
    email: str | None = None
    role: Literal["admin", "doctor", "registrar"] | None = None
    is_active: bool | None = None
    password: str | None = None


class UserPublic(UserBase):
    id: int
    created_at: datetime
