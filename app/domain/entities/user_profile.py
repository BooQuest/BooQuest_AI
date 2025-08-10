from typing import List
from pydantic import BaseModel

# 사용자 프로필 엔티티
class UserProfile(BaseModel):
    personality: str
    selected_side_hustle: str
    characteristics: List[str]
    hobbies: List[str]
    skills: List[str]
    experience_level: str
    
    def to_dict(self) -> dict:
        return {
            "personality": self.personality,
            "selected_side_hustle": self.selected_side_hustle,
            "characteristics": self.characteristics,
            "hobbies": self.hobbies,
            "skills": self.skills,
            "experience_level": self.experience_level
        } 