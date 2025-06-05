from fastapi import APIRouter
from fastapi import Depends
from db.session import get_db
from utils.security import get_cognito_client
from modules.users.schemas.user_schema import UserCreate, UserLoginCredentials
from modules.users.controllers.user_controller import get_users as get_users_ctrl, login as login_ctrl, sign_up as sign_up_ctrl

router = APIRouter()


@router.get("")
async def get_users(db=Depends(get_db)):
    return get_users_ctrl(db)


@router.post("/sign_up")
async def create_user(user: UserCreate, client=Depends(get_cognito_client), db=Depends(get_db)):
    return sign_up_ctrl(user, client=client, db=db)


@router.post("/login")
async def login(user: UserLoginCredentials, client=Depends(get_cognito_client)):
    return login_ctrl(user, client)
