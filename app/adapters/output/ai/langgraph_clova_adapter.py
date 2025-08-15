import json
from typing import Dict, Any, List, TypedDict, Optional
from app.application.ports.output.ai_sidejob_output_port import AISideJobOutputPort
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings
from app.infrastructure.services.utils.prompt_templates import PromptTemplates
from app.infrastructure.services.utils.ai_config_factory import AIConfigFactory
from langgraph.graph import StateGraph, END

from app.infrastructure.services.utils.ai_response_reader import AIResponseReader
from app.domain.entities.onboarding_profile import OnboardingProfile
from app.adapters.input.dto.side_job_response import SideJobResponse
from app.adapters.input.dto.side_job_response import SideJobItem

class SideJobTaskState(TypedDict):
    messages: Dict[str, str]
    user_profile: OnboardingProfile  
    task_ideas: List[Dict[str, Any]]
    prompt: Optional[str] = None

class LangGraphClovaAdapter(AISideJobOutputPort):
    def __init__(self):
        self.logger = get_logger("LangGraphClovaAdapter")
        self.settings = get_settings()
        self.ai_config_factory = AIConfigFactory()
        self.response_reader = AIResponseReader()
        self.workflow_for_sidejob = self._create_workflow(SideJobTaskState, self._generate_task_ideas_for_sidejob)
    
    def _create_workflow(self, state_type, handler_fn) -> StateGraph:
        workflow = StateGraph(state_type)
        workflow.add_node("generate_tasks", handler_fn)
        workflow.set_entry_point("generate_tasks")
        workflow.add_edge("generate_tasks", END)
        return workflow.compile()    
    
    async def _generate_task_ideas_for_sidejob(self, state: SideJobTaskState) -> SideJobTaskState:
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.settings.clova_x_api_key,
                base_url=self.settings.clova_x_base_url
            )

            user_profile = state['user_profile']

            # base config 사용 (성향 보정 없이)
            model_config = self.ai_config_factory.create_ai_config(
                user_profile,
                self.settings.clova_x_provider,
                self.settings.clova_x_model
            )

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

            response_content = self.response_reader.read_ai_response(
                response,
                is_streaming=model_config.streaming
            )

            try:
                parsed_data = json.loads(response_content)
                state["task_ideas"] = parsed_data.get("recommendations", [])
            except json.JSONDecodeError as e:
                self.logger.error(f"JSON 파싱 실패: {str(e)}")
                state["task_ideas"] = []

            return state

        except openai.APIConnectionError as e:
            self.logger.error(f"Clova API 연결 오류: {str(e)}")
            state["task_ideas"] = []
            return state
        except Exception as e:
            self.logger.error(f"부업 태스크 생성 실패: {str(e)}")
            state["task_ideas"] = []
            return state

    async def generate_tasks_for_sidejob(
        self,
        messages: Dict[str, str],
        onboarding_profile: OnboardingProfile
    ) -> SideJobResponse:
        try:
            initial_state = SideJobTaskState(
                messages=messages,
                user_profile=onboarding_profile,
                task_ideas=[]
            )

            result = await self.workflow_for_sidejob.ainvoke(initial_state)

            if not result["task_ideas"]:
                raise ValueError("AI 응답에서 부업 리스트가 비어 있습니다.")
            
            return SideJobResponse(
                success=True,
                message="부업 생성 완료",
                tasks=[SideJobItem(**item) for item in result["task_ideas"]],
                prompt=messages.get("content", "") 
            )

        except Exception as e:
            self.logger.error(f"부업 생성 실패: {str(e)}")
            return SideJobResponse(
                success=False,
                message=f"부업 생성 실패: {str(e)}",
                tasks=[],
                prompt=""
            )