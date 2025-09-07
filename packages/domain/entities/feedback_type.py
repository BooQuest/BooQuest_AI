"""피드백 타입 enum."""

from enum import Enum


class FeedbackType(str, Enum):
    """피드백 타입들."""
    
    LOW_PROFITABILITY = "LOW_PROFITABILITY"
    NOT_INTERESTING = "NOT_INTERESTING"
    TOO_TIME_CONSUMING = "TOO_TIME_CONSUMING"
    CHANGE_TO_OTHER = "CHANGE_TO_OTHER"
    NONE = "NONE"
    
    @property
    def label(self) -> str:
        """한국어 라벨을 반환합니다."""
        labels = {
            "LOW_PROFITABILITY": "수익성이 낮아보여요",
            "NOT_INTERESTING": "플랫폼이 마음에 들지 않아요",
            "TOO_TIME_CONSUMING": "시간이 너무 많이 들어요",
            "CHANGE_TO_OTHER": "다른걸로 바꿔주세요",
            "NONE": "없음"
        }
        return labels.get(self.value, self.value)
    
    @classmethod
    def from_input(cls, input_value: str) -> "FeedbackType":
        """입력값으로부터 FeedbackType을 찾습니다."""
        for value in cls:
            if value.label == input_value or value.value.lower() == input_value.lower():
                return value
        return cls.NONE
