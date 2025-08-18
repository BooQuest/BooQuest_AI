from pydantic import BaseModel, Field

class MissionDraft(BaseModel):
    title: str = Field(..., description="미션 제목")
    orderNo: int = Field(..., description="미션 순서 번호")
    notes: str = Field(..., description="미션 노트")
