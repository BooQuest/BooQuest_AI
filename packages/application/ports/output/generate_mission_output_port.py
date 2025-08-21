from abc import ABC, abstractmethod
from typing import Dict, List
from packages.domain.entities.mission_draft import MissionDraft
from packages.adapters.input.dto.generate_mission_request import GenerateMissionRequest

class GenerateMissionOutputPort(ABC):
    @abstractmethod
    async def generate_missions(self, messages: Dict[str, str], request: GenerateMissionRequest) -> List[MissionDraft]:
        """AI를 통해 미션을 생성하는 출력 포트"""
        pass
