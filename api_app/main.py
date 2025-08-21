"""FastAPI entry point for the AI service.

This module creates a FastAPI application, configures CORS and logging,
and registers the HTTP API routes defined in ``api_app.adapters.input.router``.
It delegates long-running AI generation tasks to a Celery worker via tasks
exposed in the ``worker_app`` package.
"""

import atexit
import os
import signal
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api_app.router import ai_router, status_router
from packages.infrastructure.config import get_settings, stop_settings_watcher
from packages.infrastructure.logging import get_logger


# FastAPI 앱 생성
app = FastAPI(
    title="AI API",
    description="부업을 통한 수입화 도우미",
    version="1.0.0",
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger = get_logger("api_app.main")

# 라우터 등록
app.include_router(ai_router)
app.include_router(status_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/show-config")
def show_config():
    """Return the current settings for inspection."""
    settings = get_settings()
    return settings.model_dump()


def cleanup() -> None:
    """Perform cleanup actions such as stopping the settings watcher."""
    stop_settings_watcher()


def signal_handler(signum: int, frame) -> None:
    cleanup()
    sys.exit(0)


# Register cleanup and signal handlers
atexit.register(cleanup)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    port = int(os.getenv("APP_PORT", "8081"))
    uvicorn.run("api_app.main:app", host="0.0.0.0", port=port, reload=True, log_level="info")