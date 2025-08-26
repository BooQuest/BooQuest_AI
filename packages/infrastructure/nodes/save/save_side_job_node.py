"""사이드잡 저장을 위한 LangGraph 노드."""

from typing import Dict, Union
from packages.infrastructure.nodes.base_node import BaseSaveNode
from packages.infrastructure.nodes.states.langgraph_state import SideJobState


class SaveSideJobNode(BaseSaveNode[SideJobState]):
    """사이드잡 저장을 위한 LangGraph 노드."""
    
    def __init__(self, uow_factory, table):
        super().__init__("save_side_jobs", uow_factory, table)
    
    def save_side_jobs(self, state: SideJobState) -> SideJobState:
        """사이드잡을 저장합니다."""
        return self.save_entities(state, "side_jobs")
    
    def _prepare_data(self, entity: Dict[str, Union[int, str, bool]], state: SideJobState) -> Dict[str, Union[int, str, bool]]:
        """저장할 데이터를 준비합니다."""
        
        return {
            "user_id": state["user_id"],
            "title": entity.get("title", ""),
            "description": entity.get("description", "설명이 제공되지 않았습니다"),
            "prompt_meta": self._safe_get_nested(state, "ai_result", "prompt_meta", default=""),
            "is_selected": False
        }