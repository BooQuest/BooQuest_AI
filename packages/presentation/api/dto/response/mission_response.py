

from pydantic import BaseModel


class MissionResponse(BaseModel):
    id: int
    title: str
    order: int
    design_notes: str
