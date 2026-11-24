from app.middleware.check_role import RoleChecker
from app.services.user_service import UserService
from app.db.models.user import UserCreate, UserUpdate, UserPublic
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserPublic)
async def create_user(dto: UserCreate, service: UserService = Depends()):
    return await service.create_user(dto)


@router.patch("/{id}/update", response_model=UserPublic)
async def update_user(
    id: int,
    dto: UserUpdate,
    service: UserService = Depends(),
    current_user=Depends(RoleChecker(["admin"])),
):
    return await service.update_user(dto, id)
