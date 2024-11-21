from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables
from .merchants.routes import router as merchants_router
from .methods.routes import router as methods_router
from .transactions.routes import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="PSP Core Backend", lifespan=lifespan)

for router in [
    merchants_router,
    methods_router,
    transactions_router,
]:
    app.include_router(router)
