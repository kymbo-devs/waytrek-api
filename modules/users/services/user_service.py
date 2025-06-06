from fastapi import HTTPException
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session

from modules.users.services import cognito_service


def create_user(user: UserCreate, client: CognitoIdentityProviderClient, db: Session):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if (user_exists): raise HTTPException(400, "An user is already registered with this email.")
    cognito_user = cognito_service.sign_up(user, client)
    new_user = User(email=user.email, cognito_id=cognito_user.get(
        'UserSub'), name=user.email.split('@')[0])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
