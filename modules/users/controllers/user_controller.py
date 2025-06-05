from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import SignUpRequestTypeDef
from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserLoginCredentials, UserCreate
import modules.users.services.cognito_service as cognito_service
from modules.users.services.user_service import create_user

def login(user: UserLoginCredentials, client: CognitoIdentityProviderClient):
    return cognito_service.login(user, client)

def sign_up(user: UserCreate, db: Session, client: CognitoIdentityProviderClient):
    create_user(user, client=client, db=db)
    return {
        "message": "Successful Sign up. Please verify your email."
    }

def get_users(db: Session):
    return db.execute(select(User)).scalars().all()
