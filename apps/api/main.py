"""FastAPI 메인 애플리케이션."""

from fastapi import FastAPI
from packages.infrastructure.di.container import container

from apps.api.routes import router


def create_app() -> FastAPI:
    """FastAPI 애플리케이션을 생성합니다."""
    app = FastAPI(title="AI API")
    
    # Container를 FastAPI 앱에 연결
    app.container = container
    
    # dependency-injector wiring 설정 - 모듈 이름으로 설정
    container.wire(modules=["apps.api.routes"])
    
    app.include_router(router)
    return app


app = create_app()
