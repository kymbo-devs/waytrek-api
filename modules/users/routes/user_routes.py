from fastapi import APIRouter
from fastapi import Depends
from db.session import get_db
from utils.security import get_cognito_client
from modules.users.schemas.user_schema import UserAuthResult, UserConfirmData, UserCreate, UserLoginCredentials
from modules.users.controllers import user_controller

router = APIRouter()


@router.get("")
async def get_users(db=Depends(get_db)):
    return user_controller.get_users(db)


@router.post("/sign_up")
async def create_user(user: UserCreate, client=Depends(get_cognito_client), db=Depends(get_db)):
    return user_controller.sign_up(user, client=client, db=db)


@router.post("/login", response_model=UserAuthResult)
async def login(user: UserLoginCredentials, client=Depends(get_cognito_client)):
    return user_controller.login(user, client)

@router.post("/confirm")
async def confirm(user: UserConfirmData, client=Depends(get_cognito_client)):
    return user_controller.confirm_user(user, client)
