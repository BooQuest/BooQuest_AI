"""사이드잡 저장을 위한 LangGraph 노드."""

from typing import Dict, Union
from packages.infrastructure.nodes.base_node import BaseSaveNode
from packages.infrastructure.nodes.states.langgraph_state import SideJobState
from packages.infrastructure.logging import get_logger


class SaveSideJobNode(BaseSaveNode[SideJobState]):
    """사이드잡 저장을 위한 LangGraph 노드."""
    
    def __init__(self, uow_factory, table):
        super().__init__("save_side_jobs", uow_factory, table)
        self.logger = get_logger(__name__)
    
    def save_side_jobs(self, state: SideJobState) -> SideJobState:
        """사이드잡을 저장합니다."""
        self.logger.info(f"[SaveSideJobNode] userId: {state.get('user_id')}")
        side_job_ids = state.get("side_job_ids", None)
        self.logger.info(f"[SaveSideJobNode] 전달된 side_job_ids: {side_job_ids}")
        state["side_job_ids"] = side_job_ids

        # ai_result에서 side_jobs 추출하고 index 주입
        side_jobs = state.get("ai_result", {}).get("side_jobs", [])
        for i, job in enumerate(side_jobs):
            job["_index"] = i
            if side_job_ids and i < len(side_job_ids):
                job["id"] = side_job_ids[i]  # 여기에 바로 ID 주입
            self.logger.info(f"[SaveSideJobNode] 주입된 _index: {i}, id: {job.get('id')}, title: {job.get('title')}")

        # 엔티티를 state에 넣어줘야 save_entities가 처리할 수 있음
        state["side_jobs"] = side_jobs

        return self.save_entities(state, "side_jobs")

    def _prepare_data(self, entity: Dict[str, Union[int, str, bool]], state: SideJobState) -> Dict[str, Union[int, str, bool]]:
        """저장할 데이터를 준비합니다."""
        
        index = entity.get("_index", None)
        side_job_ids = state.get("side_job_ids", None)

        base = {
            "user_id": state["user_id"],
            "title": entity.get("title", ""),
            "description": entity.get("description", "설명이 제공되지 않았습니다"),
            "prompt_meta": self._safe_get_nested(state, "ai_result", "prompt_meta", default=""),
            "is_selected": False,
        }

        # upsert용 ID 지정
        if side_job_ids and index is not None and index < len(side_job_ids):
            base["id"] = side_job_ids[index]

        self.logger.info(f"[SaveSideJobNode] entity index: {index}, assigned id: {base.get('id')}")

        return base