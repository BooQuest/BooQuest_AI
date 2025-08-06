"""
AI 모델 관련 도메인 객체들을 정의합니다.
"""
from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """LLM 제공자 열거형"""
    CLOVA_X = "clova_x"


class LLMModel(str, Enum):
    """LLM 모델 열거형"""
    CLOVA_X_HCX_005 = "HCX-005"


class AIModelConfig(BaseModel):
    """
    AI 모델 설정 엔티티
    """
    provider: LLMProvider = Field(..., description="AI 모델 제공자")
    model: LLMModel = Field(..., description="사용할 모델")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="생성 온도")
    max_tokens: Optional[int] = Field(default=None, ge=1, description="최대 토큰 수")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p 샘플링")
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="빈도 페널티")
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="존재 페널티")
    streaming: bool = Field(default=False, description="스트리밍 사용 여부")
    
    # 추가 설정
    model_kwargs: Dict[str, Any] = Field(default_factory=dict, description="모델별 추가 설정")


class ChatMessage(BaseModel):
    """
    채팅 메시지 엔티티
    """
    role: str = Field(..., description="메시지 역할 (system, user, assistant)")
    content: str = Field(..., description="메시지 내용")
    name: Optional[str] = Field(None, description="메시지 작성자 이름") 