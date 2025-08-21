from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, Field

@dataclass(frozen=True)
class MissionStep(BaseModel):
    # 도메인 객체/다른 클래스에서 속성으로 읽어오기 허용
    model_config = ConfigDict(from_attributes=True, extra="ignore")
    
    title: str = Field(..., description="미션 스텝 제목")
    seq: int = Field(..., description="미션 스텝 순서")
    detail: str = Field(..., description="미션 스텝 상세 내용")

