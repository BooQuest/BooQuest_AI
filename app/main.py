"""
메인 애플리케이션
FastAPI 기반 웹 서버를 실행합니다.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.adapters.input.http.ai_http_adapter import AIHttpAdapter
from app.infrastructure.logging import get_logger

# FastAPI 앱 생성
app = FastAPI(
    title="AI Chat API",
    description="AI와의 대화를 위한 API",
    version="1.0.0"
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger("main")

# HTTP 어댑터 초기화
ai_http_adapter = AIHttpAdapter()

# 라우터 등록
app.include_router(ai_http_adapter.router)

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )