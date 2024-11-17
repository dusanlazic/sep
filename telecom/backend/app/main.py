from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Telecom Backend", lifespan=lifespan)
