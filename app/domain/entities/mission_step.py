from pydantic import BaseModel, Field

class MissionStep(BaseModel):
    title: str = Field(..., description="미션 스텝 제목")
    seq: int = Field(..., description="미션 스텝 순서")
    detail: str = Field(..., description="미션 스텝 상세 내용")
