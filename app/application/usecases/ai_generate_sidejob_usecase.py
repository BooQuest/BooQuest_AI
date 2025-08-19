from typing import Dict, Any
from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
from app.application.ports.output.ai_sidejob_output_port import AISideJobOutputPort
from app.domain.entities.onboarding_profile import OnboardingProfile
from app.infrastructure.logging import get_logger
from app.infrastructure.services.utils.prompt_templates import PromptTemplates

class AIGenerateSideJobUseCase(AISideJobInputPort):
    def __init__(self, ai_output_port: AISideJobOutputPort):
        self.ai_output_port = ai_output_port
        self.logger = get_logger("AIAssistantUseCase")
    
    async def generate_side_jobs(self, onboarding_profile_request) -> Dict[str, Any]:
        # Request DTO를 Domain 엔티티로 변환
        onboarding_profile_request = OnboardingProfile(
            personality=onboarding_profile_request.personality,
            job=onboarding_profile_request.job,
            hobbies=onboarding_profile_request.hobbies,
            expressionStyle=onboarding_profile_request.expressionStyle,
            strengthType=onboarding_profile_request.strengthType
        )
        
        # 공통 프롬프트 템플릿 사용
        prompt = PromptTemplates.generate_recommendation_sidejob_prompt(onboarding_profile_request)

        messages = {"role": "user", "content": prompt}

        return await self.ai_output_port.generate_tasks_for_sidejob(messages, onboarding_profile_request)
    