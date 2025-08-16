from pydantic import BaseModel, Field

class GenerateMissionRequest(BaseModel):
    user_id: int = Field(..., description="사용자 ID")
    side_job_id: int = Field(None, description="사이드잡 ID")
    side_job_title: str = Field(..., description="사이드잡 제목")
    side_job_design_notes: str = Field(..., description="사이드잡 디자인 노트")
