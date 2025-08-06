"""
AI 입력 포트
AI와의 상호작용을 위한 인터페이스입니다.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from app.domain.entities.ai_model import AIModelConfig

class AIInputPort(ABC):
    """AI 입력 포트 인터페이스"""
    
    @abstractmethod
    async def ask_question(self, question: str, model_config: AIModelConfig) -> Dict[str, Any]:
        """
        AI에게 질문을 합니다.
        
        Args:
            question: 질문 내용
            model_config: AI 모델 설정
            
        Returns:
            AI 응답
        """
        pass 