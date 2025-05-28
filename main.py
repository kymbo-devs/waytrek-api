from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from db.session import Base, engine
from botocore.exceptions import ClientError

app = FastAPI(
    title="WayTrek API",
    description="API para la aplicación WayTrek",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

Base.metadata.create_all(bind=engine)

@app.exception_handler(ClientError)
async def client_error_handler(req, exc):
    raise HTTPException(exc.response['ResponseMetadata']['HTTPStatusCode'], exc.response.get(  # type: ignore
        'message'))

@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
