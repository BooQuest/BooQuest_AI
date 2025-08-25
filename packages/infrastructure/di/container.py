"""Dependency Injection 컨테이너."""

from dependency_injector import containers, providers
from packages.core.db.database import create_database_engine_from_config
from packages.core.external.langgraph.workflow import LangGraphWorkflowService
from packages.core.db.uow_sqlalchemy import SqlAlchemyUoW
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.logging import get_logger


class Container(containers.DeclarativeContainer):
    """애플리케이션 의존성 컨테이너."""
    
    # 설정 및 로깅
    config = providers.Singleton(get_settings)
    logger = providers.Singleton(get_logger, "app")
    
    # 데이터베이스
    database_engine = providers.Singleton(create_database_engine_from_config)
    
    # Unit of Work
    uow = providers.Factory(SqlAlchemyUoW)
    
    # LangGraph 워크플로우 (싱글톤으로 변경)
    langgraph_workflow = providers.Singleton(
        LangGraphWorkflowService,
        uow_factory=uow.provider
    )


# DI 컨테이너
container = Container()
