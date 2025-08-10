from typing import Dict, Any
from app.application.ports.input.ai_port import AIInputPort
from app.application.ports.output.ai_output_port import AIOutputPort
from app.domain.entities.user_profile import UserProfile
from app.infrastructure.logging import get_logger
from app.infrastructure.services.utils.prompt_templates import PromptTemplates

class AIAssistantUseCase(AIInputPort):
    def __init__(self, ai_output_port: AIOutputPort):
        self.ai_output_port = ai_output_port
        self.logger = get_logger("AIAssistantUseCase")
    
    async def generate_big_tasks(self, user_profile_request) -> Dict[str, Any]:
        # Request DTO를 Domain 엔티티로 변환
        user_profile = UserProfile(
            personality=user_profile_request.personality,
            selected_side_hustle=user_profile_request.selected_side_hustle,
            characteristics=user_profile_request.characteristics,
            hobbies=user_profile_request.hobbies,
            skills=user_profile_request.skills,
            experience_level=user_profile_request.experience_level
        )
        
        # 공통 프롬프트 템플릿 사용
        prompt = PromptTemplates.generate_task_prompt(user_profile)

        messages = {"role": "user", "content": prompt}
        
        return await self.ai_output_port.generate_tasks(messages, user_profile)
    