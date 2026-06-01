from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn
from pymongo import AsyncMongoClient
from config import settings

from apps.todo.routers import router as todo_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncMongoClient(
        settings.DB_URL,
        appName="farm-intro-api",
    )
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    yield
    app.mongodb_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(todo_router, tags=["tasks"], prefix="/task")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
