"""
AI HTTP DTO
AI 관련 HTTP 요청/응답 모델을 정의합니다.
"""
from pydantic import BaseModel

class AIRequest(BaseModel):
    """AI 질문 요청 모델"""
    question: str
    temperature: float = 0.7
    max_tokens: int = 1000

class AIResponse(BaseModel):
    """AI 응답 모델"""
    answer: str
    usage: dict 