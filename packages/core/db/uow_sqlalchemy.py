"""SQLAlchemy Unit of Work implementation."""

from contextlib import AbstractContextManager
from packages.infrastructure.logging import get_logger
from .database import create_database_engine_from_config

logger = get_logger(__name__)


class SqlAlchemyUoW(AbstractContextManager):
    """SQLAlchemy Unit of Work 구현체."""
    
    def __init__(self):
        """UoW 초기화."""
        # 설정에서 자동으로 연결 정보 구성
        engine = create_database_engine_from_config()
        from sqlalchemy.orm import sessionmaker
        self._maker = sessionmaker(bind=engine, expire_on_commit=False)
        logger.info("SQLAlchemy UoW 초기화 완료")
    
    def __enter__(self):
        """컨텍스트 매니저 진입."""
        self.session = self._maker()
        # Repository는 현재 구현되지 않음 - 필요시 추가 구현
        return self
    
    def __exit__(self, exc_type, exc, tb):
        """컨텍스트 매니저 종료."""
        if exc:
            self.session.rollback()
            logger.error(f"UoW 롤백: {exc}")
        else:
            self.session.commit()
            logger.debug("UoW 커밋 완료")
        self.session.close()
