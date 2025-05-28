from pydantic import BaseModel

class UserLoginCredentials(BaseModel):
    email: str
    password: str

class UserBase(UserLoginCredentials):
    pass

class UserCreate(UserBase):
    pass


