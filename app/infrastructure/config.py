"""
애플리케이션 설정
환경 변수와 설정을 관리합니다.
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # Clova X 설정
    clova_x_api_key: str = "nv-5262c448d81b44c9a5d0587c57a65bcfJod3"
    
    # 로깅 설정
    log_level: str = "INFO"
    
    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# 전역 설정 인스턴스
_settings = None

def get_settings() -> Settings:
    """설정 인스턴스를 반환합니다."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings 