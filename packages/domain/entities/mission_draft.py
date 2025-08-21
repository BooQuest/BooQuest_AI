from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, Field

@dataclass(frozen=True)
class MissionDraft(BaseModel):
    # 도메인 객체/다른 클래스에서 속성으로 읽어오기 허용
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    
    title: str = Field(..., description="미션 제목")
    orderNo: int = Field(..., description="미션 순서 번호")
    notes: str = Field(..., description="미션 노트")
