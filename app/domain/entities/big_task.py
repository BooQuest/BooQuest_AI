from pydantic import BaseModel, Field

class BigTask(BaseModel):
    title: str = Field(..., description="태스크 제목")
    description: str = Field(..., description="태스크 설명")
    difficulty: str = Field(..., description="난이도")
    priority: str = Field(..., description="우선순위")
