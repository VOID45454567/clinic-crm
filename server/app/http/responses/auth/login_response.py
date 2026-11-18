from pydantic import BaseModel, Field


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer")
