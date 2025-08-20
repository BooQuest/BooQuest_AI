from typing import List
from pydantic import BaseModel

class OnboardingProfileRequest(BaseModel):
    personality: str = "creative"
    job: str
    hobbies: List[str]
    expressionStyle:  str
    strengthType: str