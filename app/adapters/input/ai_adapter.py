"""
AI 입력 어댑터
HTTP 요청을 AI 입력 포트로 변환합니다.
"""
from typing import Dict, Any
from app.application.ports.input.ai_port import AIInputPort
from app.application.usecases.ai_usecase import AIUseCase
from app.domain.entities.ai_model import ChatMessage, AIModelConfig
from app.infrastructure.logging import get_logger

class AIAdapter(AIInputPort):
    def __init__(self, ai_use_case: AIUseCase):
        self.ai_use_case = ai_use_case
        self.logger = get_logger("AIAdapter")

    async def ask_question(self, question: str, model_config: AIModelConfig) -> Dict[str, Any]:
        """AI에게 질문을 합니다."""
        try:
            self.logger.info(f"AI 질문 요청: {question[:50]}...")
            
            # AI Use Case를 통해 질문
            response = await self.ai_use_case.ask_question(question, model_config)
            
            self.logger.info("AI 질문 응답 성공")
            return response
            
        except Exception as e:
            self.logger.error(f"AI 질문 실패: {str(e)}")
            raise 