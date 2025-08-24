"""미션 생성 요청 DTO."""

from pydantic import BaseModel, Field


class MissionGenerateRequest(BaseModel):
    """미션 생성 요청."""
    
    user_id: int  = Field(..., alias="userId")
    sidejob_id: int  = Field(..., alias="sideJobId")
    sidejob_title: str  = Field(..., alias="sideJobTitle")
    sidejob_design_notes: str  = Field(..., alias="sideJobDesignNotes")

    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"   
    }