from pydantic import AliasChoices, BaseModel, ConfigDict, Field

class GenerateMissionStepRequest(BaseModel):
    # 입력 검증 시 별칭 허용
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(
        ..., 
        validation_alias=AliasChoices("userId", "user_id")
    )
    mission_id: int = Field(
        ..., 
        validation_alias=AliasChoices("missionId", "mission_id")
    )
    mission_title: str = Field(
        ..., 
        validation_alias=AliasChoices("missionTitle", "mission_title")
    )
    mission_design_notes: str = Field(
        ..., 
        validation_alias=AliasChoices("missionDesignNotes", "mission_design_notes")
    )
