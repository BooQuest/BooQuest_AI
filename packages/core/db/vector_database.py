"""PostgreSQL Vector 확장을 위한 데이터베이스 설정."""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from packages.infrastructure.config.config import get_settings

logger = logging.getLogger(__name__)


class VectorDatabase:
    """PostgreSQL Vector 확장을 관리하는 클래스."""
    
    def __init__(self):
        self.settings = get_settings()
        self.engine = None
        self.session_factory = None
    
    def create_engine(self):
        """Vector 확장을 지원하는 엔진 생성."""
        try:
            # PostgreSQL 연결 URL 생성
            db_url = f"postgresql+psycopg2://{self.settings.DB_USER}:{self.settings.DB_PWD}@{self.settings.DB_HOST}:{self.settings.DB_PORT}/{self.settings.DB_NAME}"
            
            self.engine = create_engine(
                db_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=300
            )
            
            self.session_factory = sessionmaker(bind=self.engine)
            logger.info("Vector 데이터베이스 엔진 생성 완료")
            
        except Exception as e:
            logger.error(f"Vector 데이터베이스 엔진 생성 실패: {e}")
            raise
    
    def enable_vector_extension(self):
        """PostgreSQL에 pgvector 확장을 활성화."""
        try:
            with self.engine.connect() as conn:
                # pgvector 확장 활성화
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
                conn.commit()
                logger.info("pgvector 확장 활성화 완료")
                
        except Exception as e:
            logger.error(f"pgvector 확장 활성화 실패: {e}")
            raise
    
    def create_vector_tables(self):
        """벡터 테이블들을 생성."""
        try:
            from packages.domain.entities.sns_trend import SNSTrend, TrendEmbedding
            
            # 테이블 생성
            SNSTrend.metadata.create_all(self.engine)
            TrendEmbedding.metadata.create_all(self.engine)
            
            logger.info("벡터 테이블 생성 완료")
            
        except Exception as e:
            logger.error(f"벡터 테이블 생성 실패: {e}")
            raise
    
    def initialize(self):
        """Vector 데이터베이스 초기화."""
        try:
            self.create_engine()
            self.enable_vector_extension()
            self.create_vector_tables()
            logger.info("Vector 데이터베이스 초기화 완료")
            
        except Exception as e:
            logger.error(f"Vector 데이터베이스 초기화 실패: {e}")
            raise


# 전역 인스턴스
_vector_db: VectorDatabase = None


def get_vector_db() -> VectorDatabase:
    """Vector 데이터베이스 인스턴스 반환."""
    global _vector_db
    if _vector_db is None:
        _vector_db = VectorDatabase()
        _vector_db.initialize()
    return _vector_db
