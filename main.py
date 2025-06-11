from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from db.session import Base, engine
from botocore.exceptions import ClientError
from utils.auth_middleware import AuthMiddleware
from config import settings
from error_handlers import setup_error_handlers
import logging
from fastapi.openapi.utils import get_openapi



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url="/docs"
)

setup_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)

app.include_router(router)

Base.metadata.create_all(bind=engine)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=f"{settings.PROJECT_NAME} - API",
        version="1.0.0",
        description="Documentación de la API protegida con JWT + Cognito",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    public_paths = settings.PUBLIC_PATHS
    
    api_prefix = settings.API_PREFIX
    
    for path in openapi_schema["paths"]:
        normalized_path = path.replace(api_prefix, "")
        if normalized_path in public_paths or path == "/":
             continue

        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.exception_handler(ClientError)
async def client_error_handler(req, exc):
    raise HTTPException(exc.response['ResponseMetadata']['HTTPStatusCode'], exc.response.get(  # type: ignore
        'message'))

@app.get("/", tags=["root"])
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting Uvicorn server for {settings.PROJECT_NAME} on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
