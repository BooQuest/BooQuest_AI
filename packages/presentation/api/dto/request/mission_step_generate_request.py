"""미션 단계 생성 요청 DTO."""

from pydantic import BaseModel, Field


class MissionStepGenerateRequest(BaseModel):
    """미션 단계 생성 요청."""
    
    user_id: int = Field(..., alias="userId")
    mission_id: int = Field(..., alias="missionId")
    mission_title: str = Field(..., alias="missionTitle")
    mission_design_notes: str = Field(..., alias="missionDesignNotes")
    order_no: int = Field(..., alias="orderNo")
    side_job_title: str = Field(..., alias="sideJobTitle")
    side_job_description: str = Field(..., alias="sideJobDescription")

    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"  
    }