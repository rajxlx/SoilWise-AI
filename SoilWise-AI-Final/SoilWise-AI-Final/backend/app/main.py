from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.core.database import Base, engine
from app.models import User, Analysis  # register model metadata
from app.api import auth, analyses, voice

@asynccontextmanager
async def lifespan(_: FastAPI):
    # Local development convenience only. Production schema changes are migration-owned.
    if settings.app_env != "production":
        Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="SoilWise API", version="1.2.0",
              docs_url="/docs" if settings.app_env != "production" else None,
              redoc_url=None, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list,
                   allow_credentials=True, allow_methods=["GET", "POST"],
                   allow_headers=["Authorization", "Content-Type"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(analyses.router, prefix="/api/v1/analyses", tags=["analyses"])
app.include_router(voice.router, prefix="/api/v1/voice", tags=["voice"])

@app.get("/health", tags=["system"])
def health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
