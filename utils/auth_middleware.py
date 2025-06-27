from fastapi import Depends, Request, status
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from jose import jwt, JWTError
import requests
import logging
from functools import lru_cache
from config import settings
from typing import Callable, Awaitable, Dict, Any

from db.session import get_db
from modules.users.services import user_service

logger = logging.getLogger(__name__)

COGNITO_REGION = settings.COGNITO_USER_POOL_ID.split('_')[0]
COGNITO_USER_POOL_ID = settings.COGNITO_USER_POOL_ID
COGNITO_APP_CLIENT_ID = settings.COGNITO_CLIENT_ID

JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"

def get_user_from_request(request: Request, db=Depends(get_db)):
    return user_service.get_user_by_cognito_id(request.state.user_id, db)

@lru_cache(maxsize=1)
def get_jwks() -> Dict[str, Any]:
    try:
        response = requests.get(JWKS_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logger.error("Timeout al obtener JWKS de Cognito")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable. Please try again."
        )
    except requests.exceptions.ConnectionError:
        logger.error("Error de conexión al obtener JWKS de Cognito")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporarily unavailable. Please try again."
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not fetch JWKS for token validation."
        )

def get_public_key(token: str) -> Dict[str, str]:
    jwks = get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError as e:
        logger.warning(f"Error al obtener header no verificado del JWT: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    kid = unverified_header.get("kid")
    if not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing key ID",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unable to find appropriate key",
        headers={"WWW-Authenticate": "Bearer"},
    )

def validate_token_payload(payload: Dict[str, Any]) -> None:
    required_fields = ["sub", "exp", "iat", "token_use"]
    
    for field in required_fields:
        if field not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token missing required field: {field}",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    if payload.get("token_use") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.public_paths = {
            "/docs", 
            f"{settings.API_PREFIX}/openapi.json",
            f"{settings.API_PREFIX}/users/login",
            f"{settings.API_PREFIX}/users/sign_up",
            f"{settings.API_PREFIX}/users/confirm",
            "/",
        }

    def is_public_path(self, path: str) -> bool:
        return path in self.public_paths

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        if request.method == "OPTIONS":
            return await call_next(request)

        if self.is_public_path(request.url.path):
            return await call_next(request)

        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            token = parts[1]
            public_key = get_public_key(token)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=COGNITO_APP_CLIENT_ID,
                issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}"
            )

            validate_token_payload(payload)

            request.state.user_id = payload.get("sub")
            request.state.username = payload.get("username")
            request.state.user_payload = payload

            response = await call_next(request)
            return response

        except JWTError as e:
            logger.warning(f"Error al decodificar JWT: {e}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": {"code": 401, "message": "Invalid or expired token", "type": "authentication_error"}},
                headers={"WWW-Authenticate": "Bearer"},
            )
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": {"code": exc.status_code, "message": exc.detail, "type": "authentication_error"}},
                headers=exc.headers,
            )