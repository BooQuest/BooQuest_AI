from typing import Dict, Any
from app.application.ports.input.ai_port import AIInputPort
from app.application.ports.output.ai_port import AIOutputPort
from app.domain.entities.user_profile import UserProfile
from app.infrastructure.logging import get_logger

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
            target_income=user_profile_request.target_income,
            available_time=user_profile_request.available_time,
            skills=user_profile_request.skills,
            experience_level=user_profile_request.experience_level
        )
        
        prompt = self._create_task_generation_prompt(user_profile)
        messages = [{"role": "user", "content": prompt}]
        
        return await self.ai_output_port.generate_tasks(messages, user_profile)
    
    def _create_task_generation_prompt(self, user_profile: UserProfile) -> str:
        """큰 임무 생성 프롬프트를 생성합니다."""
        return f"""
사용자 정보를 바탕으로 {user_profile.selected_side_hustle} 부업으로 수익화할 수 있는 큰 임무들을 생성해주세요.

사용자 정보:
- 성향: {user_profile.personality}
- 선택한 부업: {user_profile.selected_side_hustle}
- 특성: {', '.join(user_profile.characteristics)}
- 취미: {', '.join(user_profile.hobbies)}
- 목표 수입: {user_profile.target_income:,}원
- 가용 시간: {user_profile.available_time}시간/주
- 보유 스킬: {', '.join(user_profile.skills)}
- 경험 수준: {user_profile.experience_level}

큰 임무들을 JSON 형태로 반환해주세요:
{{
  "big_tasks": [
    {{
      "title": "임무 제목",
      "description": "임무 설명",
      "estimated_income": "예상 수입",
      "time_required": "필요 시간",
      "difficulty": "난이도",
      "priority": "우선순위"
    }}
  ]
}}
""" 