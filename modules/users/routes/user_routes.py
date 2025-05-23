from fastapi import APIRouter
from fastapi import Depends
from db.session import get_db
from modules.users.schemas.user_schema import UserCreate
from modules.users.controllers.user_controller import get_users as get_users_ctrl, create_user as create_user_ctrl

router = APIRouter()

@router.get("")
async def get_users(db = Depends(get_db)):
    return get_users_ctrl(db)

@router.post("")
async def create_user(user: UserCreate, db = Depends(get_db)):
    return create_user_ctrl(user, db)

