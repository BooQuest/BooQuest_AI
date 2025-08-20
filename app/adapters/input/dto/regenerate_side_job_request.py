from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class FeedbackType(str, Enum):
    LOW_PROFITABILITY = "LOW_PROFITABILITY"
    NO_INTEREST = "NO_INTEREST"
    NOT_MY_STYLE = "NOT_MY_STYLE"
    TAKES_TOO_MUCH_TIME = "TAKES_TOO_MUCH_TIME"
    NOT_FEASIBLE = "NOT_FEASIBLE"
    TOO_EXPENSIVE = "TOO_EXPENSIVE"


class RegenerateFeedbackData(BaseModel):
    reasons: List[FeedbackType]
    etcFeedback: Optional[str] = None  # 기타 사유 (nullable)


class GenerateSideJobRequest(BaseModel):
    userId: int
    job: str
    hobbies: List[str]
    expressionStyle: str
    strengthType: str


class RegenerateSideJobRequest(BaseModel):
    personality: str = "creative"
    feedbackData: RegenerateFeedbackData
    generateSideJobRequest: GenerateSideJobRequest