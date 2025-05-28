import boto3
from config import settings
import hmac
import hashlib
import base64

def get_cognito_client():
    client = boto3.client('cognito-idp', region_name=settings.USER_POOL_ID.split('_')[0])
    try:
        yield client
    finally:
        client.close()



def get_secret_hash(string: str) -> str:
    msg = string + settings.CLIENT_ID
    dig = hmac.new(
        settings.CLIENT_SECRET.encode('utf-8'),
        msg=msg.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()