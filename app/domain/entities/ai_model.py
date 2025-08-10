
from typing import Optional
from pydantic import BaseModel, Field


class AIModelConfig(BaseModel):
    provider: str = Field(..., description="AI 모델 제공자")
    model: str = Field(..., description="사용할 모델")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="생성 온도")
    max_tokens: Optional[int] = Field(default=None, ge=1, description="최대 토큰 수")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p 샘플링")
    streaming: bool = Field(default=False, description="스트리밍 사용 여부")