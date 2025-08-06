"""
AI Use Case
AI 관련 비즈니스 로직을 처리합니다.
"""
from typing import Dict, Any
from app.application.ports.output.ai_port import AIPort
from app.domain.entities.ai_model import AIModelConfig, ChatMessage
from app.infrastructure.logging import get_logger

class AIUseCase:
    """AI Use Case"""
    
    def __init__(self, ai_port: AIPort):
        self.ai_port = ai_port
        self.logger = get_logger("AIUseCase")
    
    async def ask_question(self, question: str, model_config: AIModelConfig) -> Dict[str, Any]:
        """
        AI에게 질문을 합니다.
        
        Args:
            question: 질문 내용
            model_config: AI 모델 설정
            
        Returns:
            AI 응답
        """
        try:
            self.logger.info(f"AI Use Case - 질문 처리: {question[:50]}...")
            
            # 질문을 메시지로 변환
            messages = [
                ChatMessage(
                    role="user",
                    content=question
                )
            ]
            
            # AI 포트를 통해 질문
            response = await self.ai_port.chat_completion(messages, model_config)
            
            self.logger.info("AI Use Case - 질문 처리 완료")
            return response
            
        except Exception as e:
            self.logger.error(f"AI Use Case - 질문 처리 실패: {str(e)}")
            raise 