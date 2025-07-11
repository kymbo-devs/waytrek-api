from typing import List
from fastapi import APIRouter, Request, status
from fastapi import Depends
from db.session import get_db
from modules.users.schemas.saved_list_schema import SaveActivityRequest, SavedList, SavedListWithActivity
from utils.auth_middleware import get_user_from_request
from utils.security import get_cognito_client
from modules.users.schemas.user_schema import UserAuthResult, UserConfirmData, UserCreate, UserLoginCredentials, UserSignUpResponse
from modules.users.controllers import user_controller
from utils.error_models import (
    LoginErrorResponse, 
    SignUpErrorResponse,
)

router = APIRouter()


@router.get("")
async def get_users(db=Depends(get_db)):
    return user_controller.get_users(db)


@router.post(
        "/sign_up",
        response_model=UserSignUpResponse,
        status_code=status.HTTP_201_CREATED,
        responses={
            400: {"model": SignUpErrorResponse, "description": "User already exists"}
        },
        summary="Create a new user",
         description="""
Registers a new user in the system using Amazon Cognito.

- Requires a valid email address and a secure password.
- Upon successful registration, a confirmation code is sent to the user's email.
- The user must confirm their account using the received code before being able to authenticate.
""",
)
async def create_user(user: UserCreate, client=Depends(get_cognito_client), db=Depends(get_db)):
    return user_controller.sign_up(user, client=client, db=db)


@router.post("/login", 
response_model=UserAuthResult,
responses={
    400: {"model": LoginErrorResponse, "description": "Invalid credentials" },
    403: {"model": LoginErrorResponse, "description": "User not confirmed" }
},
summary="Login a user",
description="""
Logs in a user using Amazon Cognito.

- Requires a valid email address and a secure password.
- Upon successful login, a token is returned.
""",
)
async def login(user: UserLoginCredentials, client=Depends(get_cognito_client)):
    return user_controller.login(user, client)

@router.post(
    "/confirm",
    response_model=UserAuthResult,
    summary="Confirm a user",
   description="""
Confirms a user's account using Amazon Cognito.

- Accepts the user's email and a 6-digit verification code.
- This code is typically sent after registration.
- Once confirmed, the user will be able to log in using their credentials.
"""
,
)
async def confirm(user: UserConfirmData, client=Depends(get_cognito_client)):
    return user_controller.confirm_user(user, client)