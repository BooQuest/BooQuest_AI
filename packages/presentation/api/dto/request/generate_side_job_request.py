"""사이드잡 생성 요청 DTO."""

from pydantic import BaseModel, Field
from typing import List


class GenerateSideJobRequest(BaseModel):
    """사이드잡 생성 요청."""
    
    user_id: int = Field(..., alias="userId")
    job: str
    hobbies: List[str]
    expression_style: str = Field(..., alias="expressionStyle")
    strength_type: str= Field(..., alias="strengthType")


    model_config = {
        "populate_by_name": True,  # snake_case로도 채워주기 허용
        "extra": "ignore"  
    }
