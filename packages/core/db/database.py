"""Database connection and table creation utilities."""

from sqlalchemy import URL, create_engine
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.logging import get_logger

logger = get_logger(__name__)


def create_database_engine(database_url: str):
    """데이터베이스 엔진을 생성합니다."""
    try:
        # PostgreSQL 연결 최적화 설정
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            echo=False,  # SQL 로깅 비활성화 (운영환경)
            # PostgreSQL 특화 설정
            connect_args={
                "connect_timeout": 10,
                "application_name": "booquest"
            }
        )
        
        # 연결 정보 로깅 (보안을 위해 비밀번호는 마스킹)
        masked_url = database_url.replace(
            database_url.split('@')[0].split(':')[2], 
            '***'
        ) if '@' in database_url else database_url
        logger.info(f"PostgreSQL 엔진 생성 완료: {masked_url}")
        
        return engine
        
    except Exception as e:
        logger.error(f"PostgreSQL 엔진 생성 실패: {e}")
        raise


def create_database_engine_from_config():
    """설정에서 개별 값들을 읽어서 데이터베이스 엔진을 생성합니다."""
    settings = get_settings()
    
    # 개별 설정값들로 URL 구성
    url = URL.create(
        "postgresql+psycopg2",
        username=settings.DB_USER,         
        password=settings.DB_PWD,  
        host=settings.DB_HOST, 
        port=settings.DB_PORT,
        database=settings.DB_NAME
    )
    
    logger.info(f"설정 기반 PostgreSQL 연결: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    return create_database_engine(url)