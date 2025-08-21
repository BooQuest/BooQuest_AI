from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

# 사용자 프로필 엔티티
@dataclass(frozen=True)
class OnboardingProfile(BaseModel):
    personality: str
    job: str
    hobbies: List[str]
    expressionStyle:  str
    strengthType: str
    
    def to_dict(self) -> dict:
        return {
            "personality": self.personality,
            "job": self.job,
            "hobbies": self.hobbies,
            "expressionStyle": self.expressionStyle,
            "strengthType": self.strengthType,
        } 
    