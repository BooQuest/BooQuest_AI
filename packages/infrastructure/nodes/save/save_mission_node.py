"""미션 저장을 위한 LangGraph 노드."""

from typing import Dict, Union
from packages.infrastructure.nodes.base_node import BaseSaveNode
from packages.infrastructure.nodes.states.langgraph_state import MissionState


class SaveMissionNode(BaseSaveNode[MissionState]):
    """미션 저장을 위한 LangGraph 노드."""
    
    def __init__(self, uow_factory, table):
        super().__init__("save_missions", uow_factory, table)
    
    def save_missions(self, state: MissionState) -> MissionState:
        """미션을 저장합니다."""
        try:
            # 미션 저장 후 사이드잡 선택 상태 업데이트 (같은 트랜잭션에서)
            return self.save_entities(state, "missions", self._update_sidejob_selection)
        except Exception as e:
            self.logger.error(f"미션 저장 실패: {e}")
            raise
    
    def _prepare_data(self, entity: Dict[str, Union[int, str, bool]], state: MissionState) -> Dict[str, Union[int, str, bool]]:
        """저장할 데이터를 준비합니다."""
        return {
            "user_id": state["user_id"],
            "sidejob_id": state["sidejob_id"],
            "title": entity.get("title", ""),
            "order_no": entity.get("orderNo", 1),
            "design_notes": entity.get("notes", ""),
            "guide": entity.get("guide", ""),
            "status": "PLANNED"
        }
    
    def _update_sidejob_selection(self, uow, state: MissionState, saved_entities):
        """사이드잡 선택 상태를 업데이트합니다."""
        try:
            sidejob_id = state.get("sidejob_id")
            if sidejob_id:
                from packages.domain.entities.side_job import SideJob
                from sqlalchemy import update
                
                stmt = (
                    update(SideJob)
                    .where(SideJob.c.id == sidejob_id)
                    .values(is_selected=True)
                )
                uow.session.execute(stmt)
                self.logger.info(f"사이드잡 {sidejob_id} 선택 상태 업데이트 완료")
        except Exception as e:
            self.logger.error(f"사이드잡 선택 상태 업데이트 실패: {e}")
            raise
