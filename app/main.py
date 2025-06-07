from fastapi import FastAPI

from app.config import settings
from app.routers import files as files_router
from app.db import init_db, engine

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.include_router(files_router.router, prefix=settings.API_V1_STR + "/files", tags=["files"])

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}. API available at {settings.API_V1_STR}/files"
    }

@app.on_event("startup")
async def on_startup():
    print(f"🚀 Starting up {settings.PROJECT_NAME}...")
    await init_db()

@app.on_event("shutdown")
async def on_shutdown():
    print(f"🛑 Shutting down {settings.PROJECT_NAME}...")
    await engine.dispose()
