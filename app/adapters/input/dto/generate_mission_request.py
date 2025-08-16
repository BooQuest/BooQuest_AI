from pydantic import BaseModel, ConfigDict, Field

class GenerateMissionRequest(BaseModel):
    # camelCase 별칭을 허용하고, 필드 이름으로도 채울 수 있게
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(..., alias="userId", description="사용자 ID")
    side_job_id: int = Field(None, alias="sideJobId", description="사이드잡 ID")
    side_job_title: str = Field(..., alias="sideJobTitle", description="사이드잡 제목")
    side_job_design_notes: str = Field(..., alias="sideJobDesignNotes", description="사이드잡 디자인 노트")
