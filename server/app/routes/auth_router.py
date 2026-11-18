from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.db.models.user import UserPublic
from app.http.responses.auth.login_response import LoginResponse
from app.services.auth_service import AuthService, oauth_scheme

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(
    service: AuthService = Depends(),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return await service.login(form_data.username, form_data.password)


@router.get("/me", response_model=UserPublic)
async def get_me(service: AuthService = Depends(), token: str = Depends(oauth_scheme)):
    return await service.extract_user(token)
