"""
AI 포트
AI 모델과의 통신을 담당하는 인터페이스입니다.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from app.domain.entities.ai_model import ChatMessage, AIModelConfig

class AIPort(ABC):
    """AI 포트 인터페이스"""
    
    @abstractmethod
    async def chat_completion(self, messages: List[ChatMessage], model_config: AIModelConfig) -> Dict[str, Any]:
        """
        채팅 완성 생성
        
        Args:
            messages: 채팅 메시지 목록
            model_config: AI 모델 설정
            
        Returns:
            AI 응답
        """
        pass 