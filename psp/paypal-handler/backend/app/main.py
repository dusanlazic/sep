from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_tables
from .discovery import deregister, register
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    registered_service_id = None
    try:
        create_tables()
        registered_service_id = register("psp-paypal-handler", 9000)
    except Exception as e:
        deregister(registered_service_id)
        exit(1)

    yield

    if registered_service_id:
        deregister(registered_service_id)


app = FastAPI(title="Paypal Handler Backend", lifespan=lifespan)


@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}


app.include_router(router)
