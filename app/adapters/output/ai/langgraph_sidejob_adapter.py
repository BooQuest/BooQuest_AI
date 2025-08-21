import json
from typing import Dict, Any, List, TypedDict, Optional, Union
from app.application.ports.output.ai_sidejob_output_port import AISideJobOutputPort
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings
from app.infrastructure.services.utils.ai_config_factory import AIConfigFactory
from app.infrastructure.services.utils.ai_response_reader import AIResponseReader
from app.infrastructure.services.utils.prompt_templates import PromptTemplates
from app.domain.entities.onboarding_profile import OnboardingProfile
from app.domain.entities.regenerate_side_job import RegenerateSideJobRequest
from app.adapters.input.dto.side_job_response import SideJobResponse, SideJobItem
from langgraph.graph import StateGraph, END


class SideJobTaskState(TypedDict):
    messages: Dict[str, str]
    user_profile: OnboardingProfile
    task_ideas: List[Dict[str, Any]]
    prompt: Optional[str]


class RegenerateSideJobTaskState(TypedDict):
    messages: Dict[str, str]
    regenerate_request: RegenerateSideJobRequest
    task_ideas: List[Dict[str, Any]]
    prompt: Optional[str]


class LangGraphSideJobAdapter(AISideJobOutputPort):
    def __init__(self):
        self.logger = get_logger("LangGraphSideJobAdapter")
        self.settings = get_settings()
        self.ai_config_factory = AIConfigFactory()
        self.response_reader = AIResponseReader()

        self.workflow_for_sidejob = self._create_workflow(SideJobTaskState, self._generate_task_ideas_for_sidejob)
        self.workflow_for_regeneration = self._create_workflow(RegenerateSideJobTaskState, self._regenerate_task_ideas_with_feedback)

    def _create_workflow(self, state_type, handler_fn) -> StateGraph:
        workflow = StateGraph(state_type)
        workflow.add_node("generate_tasks", handler_fn)
        workflow.set_entry_point("generate_tasks")
        workflow.add_edge("generate_tasks", END)
        return workflow.compile()

    async def _generate_task_ideas_for_sidejob(self, state: SideJobTaskState) -> SideJobTaskState:
        try:
            import openai
            client = openai.OpenAI(api_key=self.settings.clova_x_api_key, base_url=self.settings.clova_x_base_url)
            model_config = self.ai_config_factory.create_ai_config(self.settings.clova_x_provider, self.settings.clova_x_model)

            api_params = {
                "model": model_config.model,
                "messages": [state["messages"]],
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "stream": model_config.streaming
            }
            if model_config.max_tokens is not None:
                api_params["max_tokens"] = model_config.max_tokens

            response = client.chat.completions.create(**api_params)
            response_content = self.response_reader.read_ai_response(response, model_config.streaming)

                        # 스트리밍이면 조립 검증
            if model_config.streaming and not self.response_reader.is_brace_balanced(response_content):
                self.logger.warning("JSON brace not balanced; trying repair once.")

            # 1차: 관용 파싱
            try:
                parsed_data = self.response_reader.parse_json_safely(response_content, self.logger)
                state["task_ideas"] = parsed_data.get("recommendations", []) if isinstance(parsed_data, dict) else []
                return state
            except Exception as e:
                self.logger.warning(f"Parse fail; try LLM repair once. err={e}")

        except Exception as e:
            self.logger.error(f"부업 태스크 생성 실패: {str(e)}")
            state["task_ideas"] = []
            return state

    async def _regenerate_task_ideas_with_feedback(self, state: RegenerateSideJobTaskState) -> RegenerateSideJobTaskState:
        try:
            import openai
            client = openai.OpenAI(api_key=self.settings.clova_x_api_key, base_url=self.settings.clova_x_base_url)
            model_config = self.ai_config_factory.create_ai_config(self.settings.clova_x_provider, self.settings.clova_x_model)

            api_params = {
                "model": model_config.model,
                "messages": [state["messages"]],
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "stream": model_config.streaming
            }
            if model_config.max_tokens is not None:
                api_params["max_tokens"] = model_config.max_tokens

            response = client.chat.completions.create(**api_params)
            response_content = self.response_reader.read_ai_response(response, model_config.streaming)

            try:
                state["task_ideas"] = json.loads(response_content).get("recommendations", [])
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON 파싱 실패: {str(e)}")
                state["task_ideas"] = []

            return state

        except Exception as e:
            self.logger.error(f"부업 재생성 실패: {str(e)}")
            state["task_ideas"] = []
            return state

    async def generate_tasks_for_sidejob(
        self,
        messages_or_request: Union[Dict[str, str], RegenerateSideJobRequest],
        onboarding_profile: Optional[OnboardingProfile] = None
    ) -> SideJobResponse:
        try:
            if isinstance(messages_or_request, dict):
                if onboarding_profile is None:
                    raise ValueError("OnboardingProfile은 필수입니다.")

                initial_state = SideJobTaskState(
                    messages=messages_or_request,
                    user_profile=onboarding_profile,
                    task_ideas=[],
                    prompt=messages_or_request.get("content", "")
                )
                result = await self.workflow_for_sidejob.ainvoke(initial_state)
                task_ideas = result["task_ideas"]
                prompt = result["prompt"] or messages_or_request.get("content", "")

            elif isinstance(messages_or_request, RegenerateSideJobRequest):
                initial_state = RegenerateSideJobTaskState(
                    messages={},
                    regenerate_request=messages_or_request,
                    task_ideas=[],
                    prompt=""
                )
                print("init", initial_state)
                result = await self.workflow_for_regeneration.ainvoke(initial_state)
                print("result", result)
                task_ideas = result["task_ideas"]
                prompt = result["prompt"]

            else:
                raise TypeError("지원하지 않는 타입입니다.")

            if not task_ideas:
                raise ValueError("AI 응답에서 부업 리스트가 비어 있습니다.")

            return SideJobResponse(
                success=True,
                message="부업 생성 완료",
                tasks=[SideJobItem(**item) for item in task_ideas],
                prompt=prompt
            )

        except Exception as e:
            self.logger.error(f"부업 생성 실패: {str(e)}")
            return SideJobResponse(
                success=False,
                message=f"부업 생성 실패: {str(e)}",
                tasks=[],
                prompt=""
            )