from typing import NotRequired
from typing_extensions import TypedDict
from pydantic import BaseModel, EmailStr, Field

class UserLoginCredentials(BaseModel):
    email: EmailStr = Field(..., example="test@example.com")
    password: str = Field(..., example="password123")

class UserBase(UserLoginCredentials):
    pass

class UserCreate(UserBase):
    pass

class UserConfirmData(BaseModel):
    email: EmailStr = Field(..., example="test@example.com")
    code: str = Field(..., example="123456")

class UserSignUpResponse(BaseModel):
    message: str = Field(..., example="Successful Sign up. Please verify your email.")

class UserAuthResult(TypedDict):
    access_token: NotRequired[str]
    expires_in: NotRequired[int]
    token_type: NotRequired[str]
    refresh_token: NotRequired[str]


