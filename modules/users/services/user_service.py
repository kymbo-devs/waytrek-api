from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from modules.users.models.user import User
from modules.users.schemas.user_schema import UserCreate
from sqlalchemy.orm import Session

from modules.users.services import cognito_service


def create_user(user: UserCreate, client: CognitoIdentityProviderClient, db: Session):
    cognito_user = cognito_service.sign_up(user, client)
    user = User(email=user.email, cognito_id=cognito_user.get(
        'UserSub'), name=user.email.split('@')[0])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
