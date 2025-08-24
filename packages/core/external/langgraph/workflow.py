"""LangGraph 워크플로우 서비스."""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from packages.infrastructure.logging import get_logger
from packages.infrastructure.nodes.mission_generation_node import MissionGenerationNode
from packages.infrastructure.nodes.mission_step_generation_node import MissionStepGenerationNode
from packages.infrastructure.nodes.regenerate_side_job_generation_node import RegenerateSideJobGenerationNode
from packages.infrastructure.nodes.save_mission_node import SaveMissionNode
from packages.infrastructure.nodes.save_mission_step_node import SaveMissionStepNode
from packages.infrastructure.nodes.save_side_job_node import SaveSideJobNode
from packages.infrastructure.nodes.side_job_generation_node import SideJobGenerationNode


class LangGraphWorkflowService:
    """LangGraph 워크플로우 서비스."""
    
    def __init__(self, uow_factory=None):
        """워크플로우 서비스 초기화."""
        self.logger = get_logger(__name__)
        self.uow_factory = uow_factory
        self.mission_workflow = self._build_mission_workflow()
        self.mission_step_workflow = self._build_mission_step_workflow()
        self.side_job_workflow = self._build_side_job_workflow()
        self.regenerate_side_job_workflow = self._build_regenerate_side_job_workflow()
        self.logger.info("LangGraph 워크플로우 서비스 초기화 완료")

    def _build_mission_workflow(self):
        """미션 생성 워크플로우를 구축합니다."""
        sg = StateGraph(dict)
        
        # AI 생성 노드
        generation_node = MissionGenerationNode()
        sg.add_node("generate_missions", generation_node)
        
        # 저장 노드 (UoW 팩토리가 있는 경우에만)
        if self.uow_factory:
            save_node = SaveMissionNode(self.uow_factory)
            sg.add_node("save_missions", save_node.save_missions)
            sg.add_edge("generate_missions", "save_missions")
            sg.add_edge("save_missions", END)
        else:
            sg.add_edge("generate_missions", END)
        
        sg.set_entry_point("generate_missions")
        return sg.compile()

    def _build_mission_step_workflow(self):
        """미션 단계 생성 워크플로우를 구축합니다."""
        sg = StateGraph(dict)
        
        # AI 생성 노드
        generation_node = MissionStepGenerationNode()
        sg.add_node("generate_mission_steps", generation_node)
        
        # 저장 노드 (UoW 팩토리가 있는 경우에만)
        if self.uow_factory:
            save_node = SaveMissionStepNode(self.uow_factory)
            sg.add_node("save_mission_steps", save_node.save_mission_steps)
            sg.add_edge("generate_mission_steps", "save_mission_steps")
            sg.add_edge("save_mission_steps", END)
        else:
            sg.add_edge("generate_mission_steps", END)
        
        sg.set_entry_point("generate_mission_steps")
        return sg.compile()

    def _build_side_job_workflow(self):
        """사이드잡 생성 워크플로우를 구축합니다."""
        sg = StateGraph(dict)
        
        # AI 생성 노드
        generation_node = SideJobGenerationNode()
        sg.add_node("generate_side_jobs", generation_node)
        
        # 저장 노드 (UoW 팩토리가 있는 경우에만)
        if self.uow_factory:
            save_node = SaveSideJobNode(self.uow_factory)
            sg.add_node("save_side_jobs", save_node.save_side_jobs)
            sg.add_edge("generate_side_jobs", "save_side_jobs")
            sg.add_edge("save_side_jobs", END)
        else:
            sg.add_edge("generate_side_jobs", END)
        
        sg.set_entry_point("generate_side_jobs")
        return sg.compile()

    def _build_regenerate_side_job_workflow(self):
        """사이드잡 재생성 워크플로우를 구축합니다."""
        sg = StateGraph(dict)
        
        # AI 재생성 노드
        generation_node = RegenerateSideJobGenerationNode()
        sg.add_node("regenerate_side_jobs", generation_node)
        
        # 저장 노드 (UoW 팩토리가 있는 경우에만)
        if self.uow_factory:
            save_node = SaveSideJobNode(self.uow_factory)
            sg.add_node("save_regenerated_side_jobs", save_node.save_side_jobs)
            sg.add_edge("regenerate_side_jobs", "save_regenerated_side_jobs")
            sg.add_edge("save_regenerated_side_jobs", END)
        else:
            sg.add_edge("regenerate_side_jobs", END)
        
        sg.set_entry_point("regenerate_side_jobs")
        return sg.compile()

    async def generate_missions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """미션을 생성합니다."""
        try:
            result = await self.mission_workflow.ainvoke({"request_data": request_data})
            return result.get("saved_missions", {})
        except Exception as e:
            self.logger.error(f"미션 생성 오류: {e}")
            raise

    async def generate_mission_steps(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """미션 단계를 생성합니다."""
        try:
            result = await self.mission_step_workflow.ainvoke({"request_data": request_data})
            return result.get("saved_mission_steps", {})
        except Exception as e:
            self.logger.error(f"미션 단계 생성 오류: {e}")
            raise

    async def generate_side_jobs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡을 생성합니다."""
        try:
            result = await self.side_job_workflow.ainvoke({"profile_data": request_data})
            return result.get("saved_side_jobs", {})
        except Exception as e:
            self.logger.error(f"사이드잡 생성 오류: {e}")
            raise

    async def regenerate_side_jobs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡을 재생성합니다."""
        try:
            result = await self.regenerate_side_job_workflow.ainvoke({"request_data": request_data})
            return result.get("regenerated_side_jobs", {})
        except Exception as e:
            self.logger.error(f"사이드잡 재생성 오류: {e}")
            raise
