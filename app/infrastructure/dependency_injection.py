"""
의존성 주입 컨테이너
애플리케이션의 의존성을 관리하고 해결합니다.
"""
from typing import Dict, Any, TypeVar, Type
from app.application.ports.output.ai_port import AIPort
from app.application.ports.input.ai_port import AIInputPort
from app.infrastructure.logging import get_logger

T = TypeVar('T')

class DependencyContainer:
    """의존성 주입 컨테이너"""
    
    def __init__(self):
        self._factories: Dict[str, Any] = {}
        self._instances: Dict[str, Any] = {}
        self.logger = get_logger("DependencyContainer")
        self._setup_dependencies()
    
    def _setup_dependencies(self):
        """의존성 설정"""
        # Output Ports (외부 시스템과의 인터페이스)
        self._factories[AIPort.__name__] = lambda: self._create_langgraph_clova_adapter()
        
        # Input Ports (애플리케이션과의 인터페이스)
        self._factories[AIInputPort.__name__] = lambda: self._create_ai_adapter()
    
    def _create_langgraph_clova_adapter(self):
        """LangGraph Clova X 어댑터 생성"""
        from app.adapters.output.ai.langgraph_clova_adapter import LangGraphClovaAdapter
        return LangGraphClovaAdapter()
    
    def _create_ai_adapter(self):
        """AI 어댑터 생성"""
        from app.adapters.input.ai_adapter import AIAdapter
        from app.application.usecases.ai_usecase import AIUseCase
        
        # AI 포트 해결
        ai_port = self.resolve(AIPort)
        
        # AI Use Case 생성
        ai_use_case = AIUseCase(ai_port)
        
        # AI 어댑터 생성
        return AIAdapter(ai_use_case)
    
    def resolve(self, dependency_type: Type[T]) -> T:
        """
        의존성을 해결합니다.
        
        Args:
            dependency_type: 의존성 타입
            
        Returns:
            의존성 인스턴스
        """
        dependency_name = dependency_type.__name__
        
        # 이미 생성된 인스턴스가 있으면 반환
        if dependency_name in self._instances:
            return self._instances[dependency_name]
        
        # 팩토리가 없으면 에러
        if dependency_name not in self._factories:
            raise ValueError(f"등록되지 않은 의존성: {dependency_name}")
        
        try:
            # 팩토리를 사용하여 인스턴스 생성
            instance = self._factories[dependency_name]()
            self._instances[dependency_name] = instance
            return instance
        except Exception as e:
            self.logger.error(f"의존성 해결 실패: {dependency_name} - {str(e)}")
            raise ValueError(f"의존성 해결 실패: {dependency_name} - {str(e)}")

# 전역 의존성 컨테이너 인스턴스
_container = None

def get_container() -> DependencyContainer:
    """전역 의존성 컨테이너를 반환합니다."""
    global _container
    if _container is None:
        _container = DependencyContainer()
    return _container

def resolve_dependency(dependency_type: Type[T]) -> T:
    """
    의존성을 해결하는 편의 함수입니다.
    
    Args:
        dependency_type: 의존성 타입
        
    Returns:
        의존성 인스턴스
    """
    container = get_container()
    return container.resolve(dependency_type) 