from typing import List
from pydantic import BaseModel

# 사용자 프로필 요청 모델
class UserProfileRequest(BaseModel):
    personality: str
    selected_side_hustle: str
    characteristics: List[str]
    hobbies: List[str]
    target_income: int
    available_time: int
    skills: List[str]
    experience_level: str

# 큰 임무 응답 모델
class BigTaskResponse(BaseModel):
    big_tasks: List[dict] 