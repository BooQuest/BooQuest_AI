from typing import List, Dict, Any
from pydantic import BaseModel

# 사용자 프로필 요청 모델
class UserProfileRequest(BaseModel):
    personality: str
    selected_side_hustle: str
    characteristics: List[str]
    hobbies: List[str]
    skills: List[str]
    experience_level: str