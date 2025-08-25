"""사이드잡 응답 DTO - 자바 서버와 일치."""

from pydantic import BaseModel


class SideJobResponse(BaseModel):
    
    id: int
    title: str
    description: str
