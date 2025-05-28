from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    DB_USER: str = os.getenv("DB_USER", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_NAME: str = os.getenv("DB_NAME", "")
    DB_PORT: str = os.getenv("DB_PORT", "")
    DB_HOSTNAME: str = os.getenv("DB_HOSTNAME", "")
    USER_POOL_ID: str = os.getenv("USER_POOL_ID", "")
    CLIENT_ID: str = os.getenv("CLIENT_ID", "")
    CLIENT_SECRET: str = os.getenv("CLIENT_SECRET", "")
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    # API
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "WayTrek API"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()