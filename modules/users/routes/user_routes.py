from fastapi import APIRouter
from modules.users.schemas.user_schema import UserCreate

router = APIRouter()

@router.get("/users")
async def get_users():
    return get_users()

@router.post("/users")
async def create_user(user: UserCreate):
    create_user(user)

