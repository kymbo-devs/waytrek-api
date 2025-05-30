from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from db.session import Base, engine

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


@app.get("/", tags=["root"])
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
