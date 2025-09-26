"""챗봇 대화 제목 생성 응답 DTO."""

from pydantic import BaseModel, Field


class TitleResponse(BaseModel):
    """챗봇 대화 제목 생성 응답."""
    title: str = Field(..., description="생성된 대화 제목")
