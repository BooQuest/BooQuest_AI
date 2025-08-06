"""
로깅 시스템 설정
애플리케이션의 로깅을 관리합니다.
"""

import logging
import sys
from typing import Optional
from app.infrastructure.config import get_settings


def setup_logging(
    log_level: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """
    로깅 시스템 초기화
    
    Args:
        log_level: 로그 레벨 (기본값: 설정에서 가져옴)
        log_format: 로그 포맷 (기본값: 설정에서 가져옴)
    
    Returns:
        설정된 로거 인스턴스
    """
    settings = get_settings()
    
    # 설정값 가져오기
    level = log_level or settings.log_level
    format_str = log_format or settings.log_format
    
    # 로거 생성
    logger = logging.getLogger("main_task_generator")
    logger.setLevel(getattr(logging, level.upper()))
    
    # 기존 핸들러 제거 (중복 방지)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # 포맷터 설정
    formatter = logging.Formatter(format_str)
    console_handler.setFormatter(formatter)
    
    # 핸들러 추가
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "main_task_generator") -> logging.Logger:
    """
    로거 인스턴스 반환
    
    Args:
        name: 로거 이름
    
    Returns:
        로거 인스턴스
    """
    return logging.getLogger(name)


# 전역 로거 인스턴스
logger = get_logger()


class LoggerMixin:
    """
    로깅 기능을 제공하는 믹스인 클래스
    """
    
    @property
    def logger(self) -> logging.Logger:
        """클래스별 로거 반환"""
        return get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}") 