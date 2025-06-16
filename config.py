from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv
import logging


load_dotenv()



class Settings(BaseSettings):
    # Database
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_PORT: str = os.getenv("DB_PORT", "")
    DB_HOSTNAME: str = os.getenv("DB_HOSTNAME", "")
    COGNITO_USER_POOL_ID: str = os.getenv("COGNITO_USER_POOL_ID", "")
    COGNITO_CLIENT_ID: str = os.getenv("COGNITO_CLIENT_ID", "")
    COGNITO_CLIENT_SECRET: str = os.getenv("COGNITO_CLIENT_SECRET", "")
    # S3
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")
    S3_REGION: str = os.getenv("S3_REGION", "")
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # API
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "WayTrek API"
    PUBLIC_PATHS: list[str] = ["/users/login", "/users/sign_up", "/users/confirm", "/docs", "/openapi.json"]

@lru_cache()
def get_settings():
    settings = Settings()
    return settings

settings = get_settings()