from abc import ABC, abstractmethod
from typing import Dict, Any

class AIInputPort(ABC):
    @abstractmethod
    async def generate_big_tasks(self, user_profile_request) -> Dict[str, Any]:
        """사용자 프로필 요청을 받아서 큰 임무들을 생성합니다."""
        pass 