"""미션 단계 응답 DTO - 자바 서버와 일치."""

from pydantic import BaseModel


class MissionStepResponse(BaseModel):
    """미션 단계 응답 - 자바 MissionStepResponseDto와 일치."""
    
    id: int
    title: str
    seq: int
    status: str
    detail: str
