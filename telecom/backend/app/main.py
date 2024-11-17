from contextlib import asynccontextmanager

from fastapi import FastAPI

from .auth.routes import router as auth_router
from .database import create_tables
from .offers.routes import router as offers_router
from .transactions.routes import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(title="Telecom Backend", lifespan=lifespan)

for router in [
    auth_router,
    offers_router,
    transactions_router,
]:
    app.include_router(router)
