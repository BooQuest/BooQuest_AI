from abc import ABC, abstractmethod

from packages.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from packages.adapters.input.dto.generate_mission_step_response import GenerateMissionStepResponse


class MissionStepGenerationInputPort(ABC):
    @abstractmethod
    async def generate_mission_steps(self, request: GenerateMissionStepRequest) -> GenerateMissionStepResponse:
        """미션 스텝 생성을 위한 입력 포트"""
        pass
