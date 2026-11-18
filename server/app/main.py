from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.conf.config import settings
from app.db.connect import engine
from app.exception_handlers import setup_exception_handlers
from app.routes.auth_router import router as auth_router

app = FastAPI(
    title="Clinic CRM API",
    description="API для управления медицинской клиникой",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_exception_handlers(app)

app.include_router(router=auth_router, prefix="/api/v1")


@app.get("/api/v1/health")
async def health_check():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": True}
    except Exception as e:
        return {"status": "degraded", "db": False, "error": str(e)}
