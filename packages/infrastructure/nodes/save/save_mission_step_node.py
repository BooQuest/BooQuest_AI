"""미션 단계 저장을 위한 LangGraph 노드."""

from typing import Dict, Union
from packages.infrastructure.nodes.base_node import BaseSaveNode
from packages.infrastructure.nodes.states.langgraph_state import MissionStepState


class SaveMissionStepNode(BaseSaveNode[MissionStepState]):
    """미션 단계 저장을 위한 LangGraph 노드."""
    
    def __init__(self, uow_factory, table):
        super().__init__("save_mission_steps", uow_factory, table)
    
    def save_mission_steps(self, state: MissionStepState) -> MissionStepState:
        """미션 단계를 저장합니다."""
        return self.save_entities(state, "mission_steps")
    
    def _prepare_data(self, entity: Dict[str, Union[int, str, bool]], state: MissionStepState) -> Dict[str, Union[int, str, bool]]:
        """저장할 데이터를 준비합니다."""
        return {
            "mission_id": state["mission_id"],
            "seq": entity.get("seq", 0),
            "title": entity.get("title", ""),
            "detail": entity.get("detail", ""),
            "status": "PLANNED"
        }