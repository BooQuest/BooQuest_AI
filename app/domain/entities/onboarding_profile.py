from typing import List
from pydantic import BaseModel

# 사용자 프로필 엔티티
class OnboardingProfile(BaseModel):
    personality: str
    job: str
    hobbies: List[str]
    desiredSideJob: str = ""
    
    def to_dict(self) -> dict:
        return {
            "personality": self.personality,
            "job": self.job,
            "hobbies": self.hobbies,
            "desiredSideJob": self.desiredSideJob
        } 
    