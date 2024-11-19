from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="PSP Core Backend", lifespan=lifespan)

for router in []:
    app.include_router(router)
