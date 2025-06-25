from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from botocore.exceptions import ClientError
import logging
import traceback
from utils.error_models import ErrorCode, create_error_response, HttpErrorResponse

logger = logging.getLogger(__name__)


def setup_error_handlers(app: FastAPI):
    @app.exception_handler(ClientError)
    async def client_error_handler(req, exc):
        raise HTTPException(
            status_code=exc.response['ResponseMetadata']['HTTPStatusCode'], 
            detail=create_error_response(
                ErrorCode.INTERNAL_SERVER_ERROR,
                exc.response.get('message', 'An AWS service error occurred')
            )
        )
    
    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"HTTP {exc.status_code}: {exc.detail} - Path: {request.url.path}")
        
        if isinstance(exc.detail, dict) and "error_code" in exc.detail:
            content = exc.detail
        else:
            error_code = ErrorCode.INTERNAL_SERVER_ERROR
            if exc.status_code == 401:
                error_code = ErrorCode.INVALID_OR_EXPIRED_TOKEN
            elif exc.status_code == 404:
                error_code = ErrorCode.ACTIVITY_NOT_FOUND
            
            content = create_error_response(error_code, str(exc.detail))
        
        return JSONResponse(
            status_code=exc.status_code,
            content=content,
            headers=getattr(exc, "headers", None)
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"Validation error - Path: {request.url.path}, Errors: {exc.errors()}")
        
        error_details = "; ".join([f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()])
        
        return JSONResponse(
            status_code=422,
            content=create_error_response(
                ErrorCode.VALIDATION_ERROR,
                f"Validation error: {error_details}"
            )
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception - Path: {request.url.path}, Error: {str(exc)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
    
        return JSONResponse(
            status_code=500,
            content=create_error_response(
                ErrorCode.INTERNAL_SERVER_ERROR,
                "Internal server error"
            )
        )

class AuthenticationError(HTTPException):
    def __init__(self, detail: str, status_code: int = 401):
        super().__init__(status_code=status_code, detail=detail)
        self.headers = {"WWW-Authenticate": "Bearer"}

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(status_code=403, detail=detail) 