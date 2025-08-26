"""사이드잡 생성 요청 DTO."""

from pydantic import BaseModel, Field
from typing import List, Optional

class GenerateSideJobRequest(BaseModel):
    user_id: int = Field(..., alias="userId")
    job: str
    hobbies: List[str]
    expression_style: str = Field(..., alias="expressionStyle")
    strength_type: str = Field(..., alias="strengthType")
    character_type: Optional[str] = Field(default=None, alias="characterType")


class ReGenerateAllSideJobRequest(BaseModel):
    side_job_ids: Optional[List[int]] = Field(default=None, alias="sideJobIds")
    generate_side_job_request: GenerateSideJobRequest = Field(..., alias="generateSideJobRequest")