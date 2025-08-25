"""피드백 타입 enum."""

from enum import Enum


class FeedbackType(str, Enum):
    """피드백 타입들."""
    
    LOW_PROFITABILITY = "LOW_PROFITABILITY"
    NO_INTEREST = "NO_INTEREST"
    NOT_MY_STYLE = "NOT_MY_STYLE"
    TAKES_TOO_MUCH_TIME = "TAKES_TOO_MUCH_TIME"
    NOT_FEASIBLE = "NOT_FEASIBLE"
    TOO_EXPENSIVE = "TOO_EXPENSIVE"
    NONE = "NONE"
    
    @property
    def label(self) -> str:
        """한국어 라벨을 반환합니다."""
        labels = {
            "LOW_PROFITABILITY": "수익성이 낮아보여요",
            "NO_INTEREST": "흥미가 생기지 않아요",
            "NOT_MY_STYLE": "성향과 맞지 않아요",
            "TAKES_TOO_MUCH_TIME": "시간이 너무 많이 필요해요",
            "NOT_FEASIBLE": "할 수 있는 일이 아니에요",
            "TOO_EXPENSIVE": "초기 비용이 부담돼요",
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
