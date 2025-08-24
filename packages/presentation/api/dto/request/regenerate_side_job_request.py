"""사이드잡 재생성 요청 DTO."""

from pydantic import BaseModel, Field
from typing import List
from packages.domain.entities.feedback_type import FeedbackType


class RegenerateFeedbackData(BaseModel):
    """재생성 피드백 데이터."""
    
    reasons: List[FeedbackType]
    etc_feedback: str = Field(..., alias="etcFeedback")

    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"   
    }


class RegenerateSideJobRequest(BaseModel):
    """사이드잡 재생성 요청."""
    
    feedback_data: RegenerateFeedbackData = Field(..., alias="feedbackData")
    generate_side_job_request: dict = Field(..., alias="generateSideJobRequest")


    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"  
    }