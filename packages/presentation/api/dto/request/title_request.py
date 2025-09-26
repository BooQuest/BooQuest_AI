"""챗봇 대화 제목 생성 요청 DTO."""

from pydantic import BaseModel, Field


class TitleRequest(BaseModel):
    """챗봇 대화 제목 생성 요청."""
    message: str = Field(..., description="첫 번째 사용자 메시지")
