import atexit
import signal
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.adapters.input.router import router
from app.infrastructure.config import get_settings
from app.infrastructure.logging import get_logger
from app.infrastructure.config import stop_settings_watcher
from app.infrastructure.dependency_injection import setup_dependencies

# 의존성 주입 설정 초기화
setup_dependencies()

# FastAPI 앱 생성
app = FastAPI(
    title="AI  API",
    description="부업을 통한 수입화 도우미",
    version="1.0.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # credentials를 False로 변경
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

logger = get_logger("main")

# 라우터 등록
app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/show-config")
def show_config():
    settings = get_settings()
    return settings.model_dump()


def cleanup():
    stop_settings_watcher()

def signal_handler(signum, frame):
    cleanup()
    sys.exit(0)

atexit.register(cleanup) # 종료 시 정리 작업 등록
signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler) # 터미널 종료

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )