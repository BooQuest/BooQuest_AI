from abc import ABC, abstractmethod
from app.domain.entities.mission_step import MissionStep
from app.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from typing import List, Dict

class MissionStepGenerationOutputPort(ABC):
    @abstractmethod
    async def generate_mission_steps(self, messages: Dict[str, str], request: GenerateMissionStepRequest) -> List[MissionStep]:
        """AI를 통해 미션 스텝을 생성하는 출력 포트"""
        pass
