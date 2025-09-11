from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import config
from .database import create_tables
from .discovery import deregister, register
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    registered_service_id = None
    try:
        create_tables()
        registered_service_id = register("psp-crypto-handler", 9000)
    except Exception as e:
        deregister(registered_service_id)
        exit(1)

    yield

    if registered_service_id:
        deregister(registered_service_id)


app = FastAPI(title="Crypto Handler Backend", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://{config.frontend_host}", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", summary="Health Check")
def health_check():
    return {"status": "ok"}


app.include_router(router)
