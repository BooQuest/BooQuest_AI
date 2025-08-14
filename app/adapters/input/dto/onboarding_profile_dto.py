from typing import List
from pydantic import BaseModel

class OnboardingProfileRequest(BaseModel):
    personality: str
    job: str
    hobbies: List[str]