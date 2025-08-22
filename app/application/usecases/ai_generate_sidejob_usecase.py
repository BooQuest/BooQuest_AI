from typing import Dict, Any
from app.application.ports.input.ai_sidejob_input_port import AISideJobInputPort
from app.application.ports.output.ai_sidejob_output_port import AISideJobOutputPort
from app.domain.entities.onboarding_profile import OnboardingProfile
from app.domain.entities.regenerate_side_job import RegenerateSideJobRequest
from app.infrastructure.logging import get_logger
from app.infrastructure.services.utils.prompt_templates import PromptTemplates
from app.infrastructure.services.utils.prompt_templates import SIDE_JOB_SYSTEM_PROMPT

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
        user_prompt = PromptTemplates.generate_recommendation_sidejob_user_prompt(onboarding_profile_request)

        messages = [
            {"role": "system", "content": SIDE_JOB_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        return await self.ai_output_port.generate_tasks_for_sidejob(messages, onboarding_profile_request)
    
    # 피드백 기반 부업 재생성
    async def regenerate_side_jobs(self, regenerate_request: RegenerateSideJobRequest) -> Dict[str, Any]:
        onboarding_profile = OnboardingProfile(
            personality=regenerate_request.personality,
            job=regenerate_request.generateSideJobRequest.job,
            hobbies=regenerate_request.generateSideJobRequest.hobbies,
            expressionStyle=regenerate_request.generateSideJobRequest.expressionStyle,
            strengthType=regenerate_request.generateSideJobRequest.strengthType
        )

        user_prompt = PromptTemplates.regenerate_sidejob_prompt_by_feedback(regenerate_request)

        messages = [
            {"role": "system", "content": SIDE_JOB_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
        return await self.ai_output_port.generate_tasks_for_sidejob(messages, onboarding_profile)