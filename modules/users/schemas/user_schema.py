from typing import NotRequired
from typing_extensions import TypedDict
from pydantic import BaseModel

class UserLoginCredentials(BaseModel):
    email: str
    password: str

class UserBase(UserLoginCredentials):
    pass

class UserCreate(UserBase):
    pass

class UserConfirmData(BaseModel):
    email: str
    code: str

class UserAuthResult(TypedDict):
    access_token: NotRequired[str]
    expires_in: NotRequired[int]
    token_type: NotRequired[str]
    refresh_token: NotRequired[str]