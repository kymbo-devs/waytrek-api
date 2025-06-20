from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from botocore.exceptions import ClientError
import logging
import traceback
from typing_extensions import TypedDict
from typing import Any, NotRequired, Sequence

logger = logging.getLogger(__name__)

class HttpErrorDetail(TypedDict):
     code: int
     message: str
     type: str
     details: NotRequired[Sequence[Any]]

class HttpErrorResponse(TypedDict):
    error: HttpErrorDetail


def setup_error_handlers(app: FastAPI):
    @app.exception_handler(ClientError)
    async def client_error_handler(req, exc):
        raise HTTPException(exc.response['ResponseMetadata']['HTTPStatusCode'], exc.response.get(  # type: ignore
        'message'))
    
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP {exc.status_code}: {exc.detail} - Path: {request.url.path}")
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.status_code,
                    "message": exc.detail,
                    "type": "authentication_error" if exc.status_code == 401 else "http_error"
                }
            },
            headers=getattr(exc, "headers", None)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error - Path: {request.url.path}, Errors: {exc.errors()}")
        
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "type": "validation_error",
                    "details": exc.errors()
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception - Path: {request.url.path}, Error: {str(exc)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": 500,
                    "message": "Internal server error",
                    "type": "server_error"
                }
            }
        )

class AuthenticationError(HTTPException):
    def __init__(self, detail: str, status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)
        self.headers = {"WWW-Authenticate": "Bearer"}

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(status_code=403, detail=detail) 