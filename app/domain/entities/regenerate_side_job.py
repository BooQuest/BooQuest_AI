from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


# 피드백 유형 Enum
class FeedbackType(str, Enum):
    LOW_PROFITABILITY = "LOW_PROFITABILITY"
    NO_INTEREST = "NO_INTEREST"
    NOT_MY_STYLE = "NOT_MY_STYLE"
    TAKES_TOO_MUCH_TIME = "TAKES_TOO_MUCH_TIME"
    NOT_FEASIBLE = "NOT_FEASIBLE"
    TOO_EXPENSIVE = "TOO_EXPENSIVE"


# 피드백 내용
class RegenerateFeedbackData(BaseModel):
    reasons: List[FeedbackType]
    etcFeedback: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "reasons": [reason.value for reason in self.reasons],
            "etcFeedback": self.etcFeedback,
        }


# 사용자 프로필
class GenerateSideJobRequest(BaseModel):
    userId: int
    job: str
    hobbies: List[str]
    expressionStyle: str
    strengthType: str

    def to_dict(self) -> dict:
        return {
            "userId": self.userId,
            "job": self.job,
            "hobbies": self.hobbies,
            "expressionStyle": self.expressionStyle,
            "strengthType": self.strengthType,
        }


# 재생성 요청 전체
class RegenerateSideJobRequest(BaseModel):
    personality: str = "creative"
    feedbackData: RegenerateFeedbackData
    generateSideJobRequest: GenerateSideJobRequest

    def to_dict(self) -> dict:
        return {
            "personality": self.personality,
            "feedbackData": self.feedbackData.to_dict(),
            "generateSideJobRequest": self.generateSideJobRequest.to_dict(),
        }