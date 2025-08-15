from typing import Type, TypeVar, Dict, Callable

T = TypeVar('T')

def get_ai_task_generator():
    from app.adapters.output.ai.langgraph_clova_adapter import LangGraphClovaAdapter
    return LangGraphClovaAdapter()

def get_ai_task_assistant():
    from app.application.usecases.ai_assistant_usecase import AIAssistantUseCase
    ai_task_generator = get_ai_task_generator()
    return AIAssistantUseCase(ai_task_generator)

def get_ai_task_sidejob_usecase():
    from app.application.usecases.ai_generate_sidejob_usecase import AIGenerateSideJobUseCase
    ai_task_generator = get_ai_task_generator()
    return AIGenerateSideJobUseCase(ai_task_generator)

_dependency_factories: Dict[Type, Callable] = {}

def register_dependency(dependency_type: Type[T], factory: Callable[[], T]) -> None:
    _dependency_factories[dependency_type] = factory

def resolve(dependency_type: Type[T]) -> T:
    if dependency_type not in _dependency_factories:
        raise ValueError(f"등록되지 않은 의존성: {dependency_type.__name__}")
    
    return _dependency_factories[dependency_type]()

def setup_dependencies():
    from app.application.ports.output.ai_output_port import AIOutputPort
    from app.application.ports.input.ai_input_port import AIInputPort
    from app.application.usecases.ai_assistant_usecase import AIAssistantUseCase
    from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
    
    register_dependency(AIOutputPort, get_ai_task_generator)
    register_dependency(AIInputPort, get_ai_task_assistant) 
    register_dependency(AISideJobInputPort, get_ai_task_sidejob_usecase)