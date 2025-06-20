from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from config import settings
from modules.users.schemas.user_schema import UserConfirmData, UserCreate, UserLoginCredentials
from utils.security import get_secret_hash
from mypy_boto3_cognito_idp.type_defs import SignUpRequestTypeDef


def login(user: UserLoginCredentials, client: CognitoIdentityProviderClient):
    return client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': user.email,
            'PASSWORD': user.password,
            'SECRET_HASH': get_secret_hash(user.email)
        },
        ClientId=settings.COGNITO_CLIENT_ID
    )

def sign_up(user: UserCreate, client: CognitoIdentityProviderClient):
    args: SignUpRequestTypeDef = {
        "ClientId": settings.COGNITO_CLIENT_ID,
        "Username": user.email,
        "Password": user.password,
        "UserAttributes": [{"Name": "email", "Value": user.email}],
        "SecretHash": get_secret_hash(user.email)
    }
    return client.sign_up(**args)

def confirm_user(data: UserConfirmData, client: CognitoIdentityProviderClient):
    return client.confirm_sign_up(
        ClientId=settings.COGNITO_CLIENT_ID,
        Username=data.email,
        ConfirmationCode=data.code,
        SecretHash=get_secret_hash(data.email)
    )
