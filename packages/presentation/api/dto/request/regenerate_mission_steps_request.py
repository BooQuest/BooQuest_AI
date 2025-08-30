from packages.presentation.api.dto.request.mission_step_generate_request import MissionStepGenerateRequest
from pydantic import BaseModel, Field
from typing import List
from packages.domain.entities.mission_step_feedback_type import MissionStepFeedbackType

class FeedbackData(BaseModel):
    """재생성 피드백 데이터."""
    
    reasons: List[MissionStepFeedbackType]
    etc_feedback: str = Field(..., alias="etcFeedback")

    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"   
    }

class RegenerateMissionStepsRequest(BaseModel):
    feedback_data: FeedbackData = Field(..., alias="feedbackData")
    mission_step_generate_request: MissionStepGenerateRequest = Field(..., alias="generateMissionStep")

    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"  
    }