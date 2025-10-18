from pydantic import BaseModel, Field

class CustomSideJobRequest(BaseModel):
    side_job: str = Field(..., alias="sideJob")