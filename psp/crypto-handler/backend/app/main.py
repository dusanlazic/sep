from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Crypto Handler Backend", lifespan=lifespan)

app.include_router(router)
