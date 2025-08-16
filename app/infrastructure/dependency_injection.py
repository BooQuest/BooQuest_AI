from typing import Type, TypeVar, Dict, Callable

T = TypeVar('T')

def get_sidejob_generator():
    from app.adapters.output.ai.langgraph_sidejob_adapter import LangGraphSideJobAdapter
    return LangGraphSideJobAdapter()

def get_ai_task_sidejob_usecase():
    from app.application.usecases.ai_generate_sidejob_usecase import AIGenerateSideJobUseCase
    ai_task_generator = get_sidejob_generator()
    return AIGenerateSideJobUseCase(ai_task_generator)

def get_mission_generater():
    from app.adapters.output.ai.langgraph_mission_adapter import LangGraphMissionAdapter
    return LangGraphMissionAdapter()

def get_mission_generation_use_case():
    from app.application.usecases.mission_generation_usecase import AIGenerateMissionUseCase
    mission_generation_adapter = get_mission_generater()
    return AIGenerateMissionUseCase(mission_generation_adapter)

_dependency_factories: Dict[Type, Callable] = {}

def register_dependency(dependency_type: Type[T], factory: Callable[[], T]) -> None:
    _dependency_factories[dependency_type] = factory

def resolve(dependency_type: Type[T]) -> T:
    if dependency_type not in _dependency_factories:
        raise ValueError(f"등록되지 않은 의존성: {dependency_type.__name__}")
    
    return _dependency_factories[dependency_type]()

def setup_dependencies():
    from app.application.ports.input.generate_mission_input_port import GenerateMissionInputPort
    from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
    
    register_dependency(AISideJobInputPort, get_ai_task_sidejob_usecase)
    register_dependency(GenerateMissionInputPort, get_mission_generation_use_case)