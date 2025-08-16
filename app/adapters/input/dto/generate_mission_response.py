from pydantic import BaseModel, Field
from typing import List
from app.domain.entities.mission_draft import MissionDraft

class GenerateMissionReponse(BaseModel):
    success: bool = Field(..., description="성공 여부")
    message: str = Field(..., description="응답 메시지")
    tasks: List[MissionDraft] = Field(..., description="미션 목록")
