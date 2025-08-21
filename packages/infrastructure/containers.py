"""
Dependency injection container using the `dependency_injector` library.

This container defines the relationships between the various outbound AI adapters
and the application use cases. Each provider constructs the necessary adapter
and use case when invoked.  Using this container eliminates the need for the
custom `dependency_injection` module and aligns with the dependency_injector
library's best practices.

The container can be instantiated once per process and reused.  Providers are
factories, so a new instance of a use case or adapter will be created each time
the provider is called.  If you need to maintain state across calls, consider
using `providers.Singleton` instead of `providers.Factory`.
"""

from dependency_injector import containers, providers

# Import outbound adapters and use cases
from packages.adapters.output.ai.langgraph_sidejob_adapter import LangGraphSideJobAdapter
from packages.adapters.output.ai.langgraph_mission_adapter import LangGraphMissionAdapter
from packages.adapters.output.ai.langgraph_mission_step_adapter import (
    LangGraphMissionStepAdapter,
)

from packages.application.usecases.ai_generate_sidejob_usecase import (
    AIGenerateSideJobUseCase,
)
from packages.application.usecases.ai_mission_generation_usecase import (
    AIGenerateMissionUseCase,
)
from packages.application.usecases.ai_mission_step_generation_usecase import (
    AIMissionStepGenerationUseCase,
)


class Container(containers.DeclarativeContainer):
    """Application's dependency injection container."""

    # Configure wiring for tasks module (optional).  You can wire specific
    # modules to enable automatic injection.  Here we leave it unset or
    # point to the worker_app tasks if using @inject.  Adjust as needed.
    # wiring_config = containers.WiringConfiguration(modules=["worker_app.tasks.ai_tasks"])

    # Outbound adapters
    sidejob_adapter = providers.Factory(LangGraphSideJobAdapter)
    mission_adapter = providers.Factory(LangGraphMissionAdapter)
    mission_step_adapter = providers.Factory(LangGraphMissionStepAdapter)

    # Use cases
    ai_sidejob_usecase = providers.Factory(
        AIGenerateSideJobUseCase,
        ai_output_port=sidejob_adapter,
    )
    generate_mission_usecase = providers.Factory(
        AIGenerateMissionUseCase,
        mission_generation_output_port=mission_adapter,
    )
    mission_step_generation_usecase = providers.Factory(
        AIMissionStepGenerationUseCase,
        mission_step_generation_output_port=mission_step_adapter,
    )
