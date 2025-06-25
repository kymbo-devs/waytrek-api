from enum import Enum
from pydantic import BaseModel


class ErrorCode(str, Enum):
    # Authentication and Authorization errors
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_NOT_CONFIRMED = "USER_NOT_CONFIRMED"
    INVALID_TOKEN_FORMAT = "INVALID_TOKEN_FORMAT"
    TOKEN_MISSING_KEY_ID = "TOKEN_MISSING_KEY_ID"
    UNABLE_TO_FIND_KEY = "UNABLE_TO_FIND_KEY"
    TOKEN_MISSING_FIELD = "TOKEN_MISSING_FIELD"
    INVALID_TOKEN_TYPE = "INVALID_TOKEN_TYPE"
    AUTHORIZATION_HEADER_MISSING = "AUTHORIZATION_HEADER_MISSING"
    INVALID_AUTHORIZATION_FORMAT = "INVALID_AUTHORIZATION_FORMAT"
    INVALID_OR_EXPIRED_TOKEN = "INVALID_OR_EXPIRED_TOKEN"
    
    # User errors
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    
    # Activity and Trip errors
    ACTIVITY_NOT_FOUND = "ACTIVITY_NOT_FOUND"
    LOCATION_NOT_FOUND = "LOCATION_NOT_FOUND"
    
    # Video upload errors
    VIDEO_UPLOAD_ERROR = "VIDEO_UPLOAD_ERROR"
    INVALID_VIDEO_TYPE = "INVALID_VIDEO_TYPE"
    VIDEO_NOT_FOUND = "VIDEO_NOT_FOUND"
    SIGNED_URL_ERROR = "SIGNED_URL_ERROR"
    VIDEO_FILE_REQUIRED = "VIDEO_FILE_REQUIRED"
    VIDEO_TITLE_REQUIRED = "VIDEO_TITLE_REQUIRED"
    VIDEO_DESCRIPTION_REQUIRED = "VIDEO_DESCRIPTION_REQUIRED"
    
    # Saved list errors
    SAVE_NOT_FOUND = "SAVE_NOT_FOUND"
    UNAUTHORIZED_DELETE = "UNAUTHORIZED_DELETE"
    
    # Service errors
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    JWKS_FETCH_ERROR = "JWKS_FETCH_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    
    # Validation errors
    VALIDATION_ERROR = "VALIDATION_ERROR"


class HttpErrorResponse(BaseModel):
    error_code: ErrorCode
    message: str


# Specific error response models by endpoint context
class LoginErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.INVALID_CREDENTIALS
    message: str = "Invalid credentials provided"
    
    class Config:
        schema_extra = {
            "examples": {
                "invalid_credentials": {
                    "summary": "Invalid Credentials",
                    "value": {
                        "error_code": "INVALID_CREDENTIALS",
                        "message": "Invalid credentials provided"
                    }
                },
                "user_not_confirmed": {
                    "summary": "User Not Confirmed",
                    "value": {
                        "error_code": "USER_NOT_CONFIRMED",
                        "message": "User account not confirmed"
                    }
                }
            }
        }


class SignUpErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.USER_ALREADY_EXISTS
    message: str = "User already exists"
    
    class Config:
        schema_extra = {
            "example": {
                "error_code": "USER_ALREADY_EXISTS",
                "message": "An user is already registered with this email."
            }
        }


class ActivityNotFoundErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.ACTIVITY_NOT_FOUND
    message: str = "Activity not found"
    
    class Config:
        schema_extra = {
            "example": {
                "error_code": "ACTIVITY_NOT_FOUND",
                "message": "Activity with id 123 not found"
            }
        }


class LocationNotFoundErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.LOCATION_NOT_FOUND
    message: str = "Location not found"
    
    class Config:
        schema_extra = {
            "example": {
                "error_code": "LOCATION_NOT_FOUND",
                "message": "Location with id 456 not found"
            }
        }


class VideoNotFoundErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.VIDEO_NOT_FOUND
    message: str = "Video not found"
    
    class Config:
        schema_extra = {
            "example": {
                "error_code": "VIDEO_NOT_FOUND",
                "message": "Video with id 789 not found for activity 123"
            }
        }


class VideoUploadErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.VIDEO_UPLOAD_ERROR
    message: str = "Video upload failed"
    
    class Config:
        schema_extra = {
            "examples": {
                "video_upload_error": {
                    "summary": "Upload Failed",
                    "value": {
                        "error_code": "VIDEO_UPLOAD_ERROR",
                        "message": "Error uploading video: File size too large"
                    }
                },
                "invalid_video_type": {
                    "summary": "Invalid Type",
                    "value": {
                        "error_code": "INVALID_VIDEO_TYPE",
                        "message": "Invalid video type. Allowed types are: video/mp4, video/quicktime, video/x-msvideo"
                    }
                },
                "video_file_required": {
                    "summary": "File Required",
                    "value": {
                        "error_code": "VIDEO_FILE_REQUIRED",
                        "message": "Video file is required"
                    }
                },
                "video_title_required": {
                    "summary": "Title Required",
                    "value": {
                        "error_code": "VIDEO_TITLE_REQUIRED",
                        "message": "Title is required"
                    }
                },
                "video_description_required": {
                    "summary": "Description Required",
                    "value": {
                        "error_code": "VIDEO_DESCRIPTION_REQUIRED",
                        "message": "Description is required"
                    }
                }
            }
        }


class SavedListErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.SAVE_NOT_FOUND
    message: str = "Save not found"
    
    class Config:
        schema_extra = {
            "examples": {
                "save_not_found": {
                    "summary": "Save Not Found",
                    "value": {
                        "error_code": "SAVE_NOT_FOUND",
                        "message": "Save with id 123 not found"
                    }
                },
                "unauthorized_delete": {
                    "summary": "Unauthorized Delete",
                    "value": {
                        "error_code": "UNAUTHORIZED_DELETE",
                        "message": "This user can't delete this save"
                    }
                }
            }
        }


class AuthTokenErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.INVALID_OR_EXPIRED_TOKEN
    message: str = "Invalid or expired token"
    
    class Config:
        schema_extra = {
            "examples": {
                "invalid_token": {
                    "summary": "Invalid Token",
                    "value": {
                        "error_code": "INVALID_OR_EXPIRED_TOKEN",
                        "message": "Invalid or expired token"
                    }
                },
                "missing_auth_header": {
                    "summary": "Missing Authorization",
                    "value": {
                        "error_code": "AUTHORIZATION_HEADER_MISSING",
                        "message": "Authorization header missing"
                    }
                },
                "invalid_auth_format": {
                    "summary": "Invalid Format",
                    "value": {
                        "error_code": "INVALID_AUTHORIZATION_FORMAT",
                        "message": "Invalid authorization header format"
                    }
                }
            }
        }


class ValidationErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.VALIDATION_ERROR
    message: str = "Validation error occurred"
    
    class Config:
        schema_extra = {
            "example": {
                "error_code": "VALIDATION_ERROR",
                "message": "Validation error: email: field required; password: field required"
            }
        }


class ServerErrorResponse(BaseModel):
    error_code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    message: str = "Internal server error"
    
    class Config:
        schema_extra = {
            "examples": {
                "internal_server_error": {
                    "summary": "Internal Server Error",
                    "value": {
                        "error_code": "INTERNAL_SERVER_ERROR",
                        "message": "Internal server error"
                    }
                },
                "service_unavailable": {
                    "summary": "Service Unavailable",
                    "value": {
                        "error_code": "SERVICE_UNAVAILABLE",
                        "message": "Service temporarily unavailable. Please try again."
                    }
                }
            }
        }
    

def create_error_response(error_code: ErrorCode, message: str) -> dict:
    return {
        "error_code": error_code.value,
        "message": message
    } 