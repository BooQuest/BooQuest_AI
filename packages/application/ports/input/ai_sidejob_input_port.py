from abc import ABC, abstractmethod
from typing import Dict, Any

class AISideJobInputPort(ABC):
    @abstractmethod
    async def generate_side_jobs(self, onboarding_profile_request) -> Dict[str, Any]:
        """사용자 온보딩 데이터를 받아서 부업들을 생성합니다."""
        pass