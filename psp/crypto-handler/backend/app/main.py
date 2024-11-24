from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import config
from .database import create_tables
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


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
