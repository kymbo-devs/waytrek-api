from fastapi import HTTPException
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from sqlalchemy import select
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from utils.error_models import ErrorCode, create_error_response
from modules.users.services import cognito_service

def create_user(user: UserCreate, client: CognitoIdentityProviderClient, db: Session):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if (user_exists): 
        raise HTTPException(
            status_code=400, 
            detail=create_error_response(
                ErrorCode.USER_ALREADY_EXISTS,
                "An user is already registered with this email."
            )
        )
    cognito_user = cognito_service.sign_up(user, client)
    new_user = User(email=user.email, cognito_id=cognito_user.get(
        'UserSub'), name=user.email.split('@')[0])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user_by_cognito_id(cognito_id: str, db: Session) -> User | None:
    return db.execute(select(User).where(User.cognito_id == cognito_id)).scalar_one_or_none()
