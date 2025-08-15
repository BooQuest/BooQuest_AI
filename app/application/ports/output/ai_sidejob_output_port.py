from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.entities.onboarding_profile import OnboardingProfile

class AISideJobOutputPort(ABC):
    @abstractmethod
    async def generate_tasks_for_sidejob(self, messages: Dict[str, str], onboarding_profile: OnboardingProfile) -> Dict[str, Any]:
        """AI를 사용하여 부업을 생성합니다."""
        pass
    