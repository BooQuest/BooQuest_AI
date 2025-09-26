"""LangGraph 워크플로우 서비스."""

from typing import Any, Dict
from langgraph.graph import StateGraph, END
from packages.infrastructure.logging import get_logger

from packages.domain.entities.side_job import SideJob
from packages.domain.entities.mission import Mission
from packages.domain.entities.mission_step import MissionStep
from packages.infrastructure.nodes.generation.mission_generation_node import MissionGenerationNode
from packages.infrastructure.nodes.generation.mission_step_generation_node import MissionStepGenerationNode
from packages.infrastructure.nodes.generation.regenerate_side_job_generation_node import RegenerateSideJobGenerationNode
from packages.infrastructure.nodes.generation.side_job_generation_node import SideJobGenerationNode
from packages.infrastructure.nodes.save.save_mission_node import SaveMissionNode
from packages.infrastructure.nodes.save.save_mission_step_node import SaveMissionStepNode
from packages.infrastructure.nodes.save.save_side_job_node import SaveSideJobNode
from packages.infrastructure.nodes.generation.mission_step_regeneration_node import MissionStepRegenerationNode
from packages.infrastructure.nodes.generation.chat_generation_node import ChatGenerationNode
from packages.infrastructure.nodes.generation.chat_classify_node import ChatClassifyNode
from packages.infrastructure.nodes.generation.chat_title_generation_node import ChatTitleGenerationNode


class LangGraphWorkflowService:
    """LangGraph 워크플로우 서비스."""
    
    def __init__(self, uow_factory):
        """워크플로우 서비스 초기화."""
        self.logger = get_logger(__name__)
        self.uow_factory = uow_factory
        
        # 워크플로우 구축
        self.mission_workflow = self._build_mission_workflow()
        self.mission_step_workflow = self._build_mission_step_workflow()
        self.side_job_workflow = self._build_side_job_workflow()
        self.regenerate_side_job_workflow = self._build_regenerate_side_job_workflow()
        self.regenerate_all_side_jobs_workflow = self._build_regenerate_all_side_job_workflow()
        self.regenerate_mission_steps_workflow = self._build_regenerate_mission_step_workflow()
        self.chat_workflow = self._build_chat_workflow()
        self.title_workflow = self._build_title_workflow()
        
        self.logger.info("LangGraph 워크플로우 서비스 초기화 완료")

    def _create_initial_state(self, **kwargs) -> Dict[str, Any]:
        """공통 초기 상태를 생성합니다."""
        return {
            "ai_result": None,
            "saved_entities": None,
            **kwargs
        }

    def _build_mission_workflow(self):
        """미션 생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import MissionState
        
        sg = StateGraph(MissionState)
        
        # AI 생성 노드
        generation_node = MissionGenerationNode()
        sg.add_node(generation_node.name, generation_node)
        
        # 저장 노드
        save_node = SaveMissionNode(self.uow_factory, Mission)
        sg.add_node(save_node.name, save_node.save_missions)
        
        # 엣지 연결
        sg.add_edge(generation_node.name, save_node.name)
        sg.add_edge(save_node.name, END)
        
        sg.set_entry_point(generation_node.name)
        return sg.compile()

    def _build_mission_step_workflow(self):
        """미션 단계 생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import MissionStepState
        
        sg = StateGraph(MissionStepState)
        
        # AI 생성 노드
        generation_node = MissionStepGenerationNode()
        sg.add_node(generation_node.name, generation_node)
        
        # 저장 노드
        save_node = SaveMissionStepNode(self.uow_factory, MissionStep)
        sg.add_node(save_node.name, save_node.save_mission_steps)
        
        # 엣지 연결
        sg.add_edge(generation_node.name, save_node.name)
        sg.add_edge(save_node.name, END)
        
        sg.set_entry_point(generation_node.name)
        return sg.compile()

    def _build_side_job_workflow(self):
        """사이드잡 생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import SideJobState
        
        sg = StateGraph(SideJobState)
        
        # AI 생성 노드
        generation_node = SideJobGenerationNode()
        sg.add_node(generation_node.name, generation_node)
        
        # 저장 노드
        save_node = SaveSideJobNode(self.uow_factory, SideJob)
        sg.add_node(save_node.name, save_node.save_side_jobs)
        
        # 엣지 연결
        sg.add_edge(generation_node.name, save_node.name)
        sg.add_edge(save_node.name, END)
        
        sg.set_entry_point(generation_node.name)
        return sg.compile()

    def _build_regenerate_side_job_workflow(self):
        """사이드잡 재생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import SideJobState
        
        sg = StateGraph(SideJobState)
        
        # AI 재생성 노드
        generation_node = RegenerateSideJobGenerationNode()
        sg.add_node(generation_node.name, generation_node)
        
        # 저장 노드
        save_node = SaveSideJobNode(self.uow_factory, SideJob)
        sg.add_node(save_node.name, save_node.save_side_jobs)
        
        # 엣지 연결
        sg.add_edge(generation_node.name, save_node.name)
        sg.add_edge(save_node.name, END)
        
        sg.set_entry_point(generation_node.name)
        return sg.compile()
    

    def _build_regenerate_all_side_job_workflow(self):
        """사이드잡 전체 재생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import SideJobState

        sg = StateGraph(SideJobState)

        generation_node = SideJobGenerationNode()
        sg.add_node(generation_node.name, generation_node)

        save_node = SaveSideJobNode(self.uow_factory, SideJob)
        sg.add_node(save_node.name, save_node.save_side_jobs)

        sg.add_edge(generation_node.name, save_node.name)
        sg.add_edge(save_node.name, END)

        sg.set_entry_point(generation_node.name)
        return sg.compile()
    

    def _build_regenerate_mission_step_workflow(self):
        """부퀘스트 재생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import RegenerateMissionStepState
        
        sg = StateGraph(RegenerateMissionStepState)
        
        # AI 생성 노드
        generation_node = MissionStepRegenerationNode()
        sg.add_node(generation_node.name, generation_node)
        
        # 저장 노드
        save_node = SaveMissionStepNode(self.uow_factory, MissionStep)
        sg.add_node(save_node.name, save_node.save_mission_steps)
        
        # 엣지 연결
        sg.add_edge(generation_node.name, save_node.name)
        sg.add_edge(save_node.name, END)
        
        sg.set_entry_point(generation_node.name)
        return sg.compile()

    def _build_chat_workflow(self):
        """부업 가이드 챗봇 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import ChatState

        sg = StateGraph(ChatState)

        generation_node = ChatGenerationNode()
#         classify_node = ChatClassifyNode(generation_node.llm)

        def _get_state_value(state: ChatState, key: str, default=None):
            if isinstance(state, dict):
                return state.get(key, default)
            return getattr(state, key, default)

        def _update_state(state: ChatState, updates):
            if isinstance(state, dict):
                new_state = dict(state)
                new_state.update(updates)
                return new_state
            for k, v in updates.items():
                setattr(state, k, v)
            return state

        def _route_chat(state: ChatState) -> str:
            is_relevant = _get_state_value(state, "is_relevant", False)
            return "generate" if is_relevant else "irrelevant"

        def _handle_irrelevant(state: ChatState) -> ChatState:
            payload = {
                "message": "부업과 관련된 질문을 해주세요."
            }
            return _update_state(state, {"ai_result": payload})

#         sg.add_node(classify_node.name, classify_node)
        sg.add_node(generation_node.name, generation_node)
#         sg.add_node("chat_request_related", _handle_irrelevant)

#         sg.add_conditional_edges(
#             classify_node.name,
#             _route_chat,
#             {
#                 "generate": generation_node.name,
#                 "irrelevant": "chat_request_related",
#             },
#         )

        sg.add_edge(generation_node.name, END)
#         sg.add_edge("chat_request_related", END)

#         sg.set_entry_point(classify_node.name)
        sg.set_entry_point(generation_node.name)
        return sg.compile()

    def _build_title_workflow(self):
        """챗봇 대화 제목 생성 워크플로우를 구축합니다."""
        from packages.infrastructure.nodes.states.langgraph_state import TitleState
        
        sg = StateGraph(TitleState)
        
        generation_node = ChatTitleGenerationNode()
        sg.add_node(generation_node.name, generation_node)
        
        sg.add_edge(generation_node.name, END)
        sg.set_entry_point(generation_node.name)
        return sg.compile()

    async def generate_missions(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """미션을 생성합니다."""
        try:
            initial_state = self._create_initial_state(
                request_data=request_data,
                user_id=request_data.get("user_id"),
                sidejob_id=request_data.get("side_job_id")
            )

            result = await self.mission_workflow.ainvoke(initial_state)
            return result.get("saved_entities", [])
        except Exception as e:
            self.logger.error(f"미션 생성 오류: {e}")
            raise

    async def generate_mission_steps(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """미션 단계를 생성합니다."""
        try:
            initial_state = self._create_initial_state(
                request_data=request_data,
                mission_id=request_data.get("mission_id")
            )
            result = await self.mission_step_workflow.ainvoke(initial_state)
            return result.get("saved_entities", [])
        except Exception as e:
            self.logger.error(f"미션 단계 생성 오류: {e}")
            raise

    async def generate_side_jobs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡을 생성합니다."""
        try:
            initial_state = self._create_initial_state(
                profile_data=request_data,
                user_id=request_data.get("user_id")
            )
            
            result = await self.side_job_workflow.ainvoke(initial_state)
            saved_entities = result.get("saved_entities", [])
            
            return saved_entities
        except Exception as e:
            self.logger.error(f"사이드잡 생성 실패: {e}")
            raise

    async def regenerate_all_side_jobs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡 전체 재생성 (기존 ID 재사용하여 upsert)."""
        try:
            generate_request = request_data.get("generate_side_job_request", {})
            sidejob_ids = request_data.get("side_job_ids", []) 

            initial_state = self._create_initial_state(
                profile_data=generate_request,
                user_id=generate_request.get("user_id"),
                side_job_ids=sidejob_ids  
            )

            result = await self.regenerate_all_side_jobs_workflow.ainvoke(initial_state)
            return result.get("saved_entities", [])
        except Exception as e:
            self.logger.error(f"사이드잡 전체 재생성 실패: {e}")
            raise

    async def regenerate_side_job(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡을 재생성합니다."""
        try:
            # SideJobRegenerateRequest 구조에 맞게 데이터 변환
            profile_data = request_data.get("generate_side_job_request", {})
            feedback_data = request_data.get("feedback_data", {})
            sidejob_id = request_data.get("side_job_id")
            
            # 피드백 정보를 profile_data에 추가
            profile_data.update({
                "feedback_reasons": [reason.value for reason in feedback_data.get("reasons", [])],
                "etc_feedback": feedback_data.get("etc_feedback", "")
            })
            
            initial_state = self._create_initial_state(
                profile_data=profile_data,
                user_id=profile_data.get("userId"),
                side_job_ids=[sidejob_id] if sidejob_id else None
            )

             # AI 재생성 및 저장
            result = await self.regenerate_side_job_workflow.ainvoke(initial_state)
            return result.get("saved_entities", [])[0]
        except Exception as e:
            self.logger.error(f"사이드잡 재생성 실패: {e}")
            raise

    async def regenerate_mission_steps(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """부퀘스트 전체 재생성."""
        try:
            generate_request = request_data.get("mission_step_generate_request", {})
            feedback_data = request_data.get("feedback_data", {}) 

            initial_state = self._create_initial_state(
                request_data=generate_request,
                reasons=feedback_data.get("reasons", []),
                etc_feedback=feedback_data.get("etc_feedback", ""),
                mission_id=generate_request.get("mission_id")
            )

            result = await self.regenerate_mission_steps_workflow.ainvoke(initial_state)
            return result.get("saved_entities", [])
        except Exception as e:
            self.logger.error(f"부퀘스트 전체 재생성 실패: {e}")
            raise

    async def chat(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """챗봇 응답을 생성합니다."""
        try:
            initial_state = self._create_initial_state(
                request_data=request_data,
                user_id=request_data.get("user_id"),
            )
            result = await self.chat_workflow.ainvoke(initial_state)
            return result.get("ai_result", {})
        except Exception as e:
            self.logger.error(f"챗봇 응답 생성 실패: {e}")
            raise

    async def generate_title(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """챗봇 대화 제목을 생성합니다."""
        try:
            initial_state = self._create_initial_state(
                request_data=request_data,
                user_id=request_data.get("user_id"),
            )
            result = await self.title_workflow.ainvoke(initial_state)
            return result.get("ai_result", {})
        except Exception as e:
            self.logger.error(f"챗봇 제목 생성 실패: {e}")
            raise