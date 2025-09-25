"""챗봇 대화 요청 DTO."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ChatTurn(BaseModel):
    role: str = Field(..., description="역할: user|assistant")
    content: str = Field(..., description="메시지 내용")


class ChatRequest(BaseModel):
    """챗봇 대화 요청."""
    user_id: Optional[int] = Field(default=None, alias="userId")
    message: str = Field(..., alias="message")
    history: List[ChatTurn] = Field(default_factory=list, alias="history")

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
    }
