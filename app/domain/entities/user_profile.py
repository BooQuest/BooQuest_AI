from typing import List
from pydantic import BaseModel

# 사용자 프로필 엔티티
class UserProfile(BaseModel):
    personality: str
    selected_side_hustle: str
    characteristics: List[str]
    hobbies: List[str]
    target_income: int
    available_time: int
    skills: List[str]
    experience_level: str
    
    def to_dict(self) -> dict:
        return {
            "personality": self.personality,
            "selected_side_hustle": self.selected_side_hustle,
            "characteristics": self.characteristics,
            "hobbies": self.hobbies,
            "target_income": self.target_income,
            "available_time": self.available_time,
            "skills": self.skills,
            "experience_level": self.experience_level
        } 