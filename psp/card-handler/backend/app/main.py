from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables
from .populate import create_banks
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    create_banks()
    yield


app = FastAPI(title="Card Handler Backend", lifespan=lifespan)


@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}


app.include_router(router)
