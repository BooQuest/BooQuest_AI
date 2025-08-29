"""미션 스텝 피드백 타입 enum."""

from enum import Enum


class MissionStepFeedbackType(str, Enum):
    """피드백 타입들."""

    TOO_DIFFICULT = "TOO_DIFFICULT"
    TOO_EASY = "TOO_EASY"
    NOT_MY_CHOICE = "NOT_MY_CHOICE"
    NOT_MATCHING_GOAL = "NOT_MATCHING_GOAL"
    NONE = "NONE"

    @property
    def label(self) -> str:
        """한국어 라벨 반환."""
        labels = {
            "TOO_DIFFICULT": "너무 어려워요",
            "TOO_EASY": "너무 쉬워요",
            "NOT_MY_CHOICE": "제가 선택한 부업과 맞지 않아요",
            "NOT_MATCHING_GOAL": "목표와 어울리지 않아요",
            "NONE": "없음"
        }
        return labels.get(self.value, self.value)

    @classmethod
    def from_input(cls, input_value: str) -> "MissionStepFeedbackType":
        """입력값으로부터 enum 값 매핑."""
        for value in cls:
            if value.label == input_value or value.value.lower() == input_value.lower():
                return value
        return cls.NONE