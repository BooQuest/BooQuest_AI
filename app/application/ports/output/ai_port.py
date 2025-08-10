from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.domain.entities.user_profile import UserProfile

class AIOutputPort(ABC):
    @abstractmethod
    async def generate_tasks(self, messages: List[Dict[str, str]], user_profile: UserProfile) -> Dict[str, Any]:
        """AI를 사용하여 태스크를 생성합니다."""
        pass 