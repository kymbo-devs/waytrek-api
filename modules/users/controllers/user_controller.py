from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import SignUpRequestTypeDef
from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserLoginCredentials, UserCreate
from config import settings
from utils.security import get_secret_hash

def login(user: UserLoginCredentials, client: CognitoIdentityProviderClient):
    return client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': user.email,
            'PASSWORD': user.password,
            'SECRET_HASH': get_secret_hash(user.email)
        },
        ClientId=settings.CLIENT_ID
    )

def sign_up(user: UserCreate, client: CognitoIdentityProviderClient):
    args: SignUpRequestTypeDef = {
        "ClientId": settings.CLIENT_ID,
        "Username": user.email,
        "Password": user.password,
        "UserAttributes": [{"Name": "email", "Value": user.email}],
        "SecretHash": get_secret_hash(user.email)
    }
    client.sign_up(**args)
    return {
        "message": "Successful Sign up. Please verify your email."
    }


def get_users(db: Session):
    return db.execute(select(User)).scalars().all()
