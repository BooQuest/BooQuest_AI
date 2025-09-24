"""챗봇 대화 응답 DTO."""

from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    message: str = Field(..., description="챗봇 응답 메시지")
