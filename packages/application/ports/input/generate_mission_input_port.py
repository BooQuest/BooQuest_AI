from abc import ABC, abstractmethod

from packages.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from packages.adapters.input.dto.generate_mission_response import GenerateMissionReponse

class GenerateMissionInputPort(ABC):
    @abstractmethod
    async def generate_missions(self, request: GenerateMissionRequest) -> GenerateMissionReponse:
        """미션 생성을 위한 입력 포트"""
        pass
