"""온보딩 프로필 도메인 엔티티 - 가이드 기준."""

from dataclasses import dataclass
from typing import List


@dataclass
class OnboardingProfile:
    """온보딩 프로필 도메인 엔티티."""
    
    user_id: int
    nickname: str
    job: str
    hobbies: List[str]
    expression_style: str
    strength_type: str
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환."""
        return {
            "user_id": self.user_id,
            "nickname": self.nickname,
            "job": self.job,
            "hobbies": self.hobbies,
            "expression_style": self.expression_style,
            "strength_type": self.strength_type,
        } 
    