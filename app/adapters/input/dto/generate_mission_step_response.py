from pydantic import BaseModel, Field
from typing import List
from app.domain.entities.mission_step import MissionStep

class GenerateMissionStepResponse(BaseModel):
    success: bool = Field(..., description="성공 여부")
    message: str = Field(..., description="응답 메시지")
    steps: List[MissionStep] = Field(..., description="미션 스텝 목록")
