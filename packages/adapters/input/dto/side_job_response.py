from pydantic import BaseModel
from typing import List, Optional

# 부업 데이터 응답 DTO
class SideJobItem(BaseModel):
    title: str
    description: str

class SideJobResponse(BaseModel):
    success: bool
    message: str
    tasks: List[SideJobItem]
    prompt: Optional[str] = ""
    