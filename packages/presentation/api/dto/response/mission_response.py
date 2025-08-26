

from pydantic import BaseModel


class MissionResponse(BaseModel):
    id: int
    title: str
    order: int
    design_notes: str
    status: str = "PLANNED"  # 기본값 설정
