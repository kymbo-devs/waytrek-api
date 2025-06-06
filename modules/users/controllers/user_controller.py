from fastapi import HTTPException
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import SignUpRequestTypeDef
from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserAuthResult, UserConfirmData, UserLoginCredentials, UserCreate
from modules.users.services import user_service
from modules.users.services import cognito_service


def login(user: UserLoginCredentials, client: CognitoIdentityProviderClient) -> UserAuthResult:
    auth_result = cognito_service.login(user, client)["AuthenticationResult"]
    return {
        "access_token": auth_result["AccessToken"], # type: ignore
        "expires_in": auth_result["ExpiresIn"], # type: ignore
        "refresh_token": auth_result["RefreshToken"], # type: ignore
        "token_type": auth_result["TokenType"] # type: ignore
    }


def sign_up(user: UserCreate, db: Session, client: CognitoIdentityProviderClient):
    user_service.create_user(user, client=client, db=db)
    return {
        "message": "Successful Sign up. Please verify your email."
    }


def get_users(db: Session):
    return db.execute(select(User)).scalars().all()


def confirm_user(user: UserConfirmData, client: CognitoIdentityProviderClient):
    cognito_service.confirm_user(user, client)
    return {
        "message": "User confirmed."
    }
