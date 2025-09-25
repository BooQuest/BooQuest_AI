"""챗봇 대화 응답 DTO."""

from pydantic import BaseModel, Field


class ChatUsage(BaseModel):
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    model: str | None = None

class ChatResponse(BaseModel):
    message: str
    usage: ChatUsage | None = None
