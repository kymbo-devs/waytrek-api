from fastapi import HTTPException
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from sqlalchemy import select
from sqlalchemy.orm import Session
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session
from config import settings
from utils.error_models import ErrorCode, create_error_response
from modules.users.constants import get_default_group, is_valid_group
from modules.users.services import cognito_service

COGNITO_USER_POOL_ID = settings.COGNITO_USER_POOL_ID

def create_user(user: UserCreate, client: CognitoIdentityProviderClient, db: Session):
    user_exists = db.query(User).filter(User.email == user.email).first()
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                ErrorCode.USER_ALREADY_EXISTS,
                "A user is already registered with this email."
            )
        )    
    cognito_user = cognito_service.sign_up(user, client)
    cognito_user_sub = cognito_user.get('UserSub')
 
    if user.cognito_group_id and not is_valid_group(user.cognito_group_id):
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                ErrorCode.VALIDATION_ERROR,
                f"Invalid group: {user.cognito_group_id}. Valid groups are: GENERAL_USER, ADMIN"
            )
        )
    
    try:
        group_to_assign = user.cognito_group_id or get_default_group()
        client.admin_add_user_to_group(
            UserPoolId=COGNITO_USER_POOL_ID, 
            Username=user.email,
            GroupName=group_to_assign
        )
    except client.exceptions.ClientError as e:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                ErrorCode.USER_GROUP_ADDITION_FAILED,
                "Failed to add user to a group."
            )
        )
    
    new_user = User(
        email=user.email, 
        cognito_id=cognito_user_sub, 
        name=user.email.split('@')[0], 
        cognito_group_id=user.cognito_group_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def get_user_by_cognito_id(cognito_id: str, db: Session) -> User | None:
    return db.execute(select(User).where(User.cognito_id == cognito_id)).scalar_one_or_none()
