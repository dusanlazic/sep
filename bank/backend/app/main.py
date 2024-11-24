from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables
from .populate import create_merchants
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    create_merchants()
    yield


app = FastAPI(title="Bank Backend", lifespan=lifespan)


@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}


app.include_router(router)
