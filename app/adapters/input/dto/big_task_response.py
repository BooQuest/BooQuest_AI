from typing import List, Dict, Any
from pydantic import BaseModel

# 큰 임무 응답 모델 (HTTP 어댑터 계층용 DTO)
class BigTaskResponse(BaseModel):
    success: bool
    big_tasks: List[Dict[str, Any]]
    message: str