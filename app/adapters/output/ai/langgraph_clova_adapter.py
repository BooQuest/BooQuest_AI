from typing import Dict, Any, List, TypedDict
from app.application.ports.output.ai_port import AIOutputPort
from app.domain.entities.user_profile import UserProfile
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings
from app.infrastructure.services.ai_config_factory import AIConfigFactory
from app.infrastructure.services.prompt_templates import PromptTemplates
from langgraph.graph import StateGraph, END
import json

class TaskState(TypedDict):
    messages: List[Dict[str, str]]
    user_profile: UserProfile
    task_ideas: List[Dict[str, Any]]

class LangGraphClovaAdapter(AIOutputPort):
    def __init__(self):
        self.logger = get_logger("LangGraphClovaAdapter")
        self.settings = get_settings()
        self.ai_config_factory = AIConfigFactory()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(TaskState)
        
        workflow.add_node("generate_tasks", self._generate_task_ideas)
        workflow.set_entry_point("generate_tasks")
        workflow.add_edge("generate_tasks", END)
        
        return workflow.compile()
    
    async def _generate_task_ideas(self, state: TaskState) -> TaskState:
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.settings.clova_x_api_key,
                base_url=self.settings.clova_x_base_url
            )
            
            # UserProfile 객체를 직접 사용
            user_profile = state['user_profile']
            
            # 공통 프롬프트 템플릿 사용
            prompt = PromptTemplates.generate_task_prompt(user_profile)
            
            # AI 설정 생성
            model_config = self.ai_config_factory.create_ai_config(
                user_profile,
                self.settings.clova_x_provider,
                self.settings.clova_x_model
            )
            
            # API 호출 파라미터 준비
            api_params = {
                "model": model_config.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "stream": model_config.streaming
            }
            
            # max_tokens가 None이 아닌 경우에만 추가
            if model_config.max_tokens is not None:
                api_params["max_tokens"] = model_config.max_tokens
            
            self.logger.info(f"Clova API 호출 파라미터: {api_params}")
            
            response = client.chat.completions.create(**api_params)
            content = response.choices[0].message.content
            
            # JSON 응답 파싱
            data = json.loads(content)
            state["task_ideas"] = data.get("big_tasks", [])
            
        except openai.APIConnectionError as e:
            self.logger.error(f"Clova API 연결 오류: {str(e)}")
            state["task_ideas"] = []
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON 파싱 실패: {str(e)}")
            state["task_ideas"] = []
        except Exception as e:
            self.logger.error(f"태스크 생성 실패: {str(e)}")
            state["task_ideas"] = []
        
        return state
    
    async def generate_tasks(self, messages: List[Dict[str, str]], user_profile: UserProfile) -> Dict[str, Any]:
        try:
            # TaskState에 user_profile을 직접 넣어줌
            initial_state = TaskState(
                messages=messages,
                user_profile=user_profile,  # UserProfile 객체를 직접 사용!
                task_ideas=[]
            )
            
            final_state = await self.workflow.ainvoke(initial_state)
            
            return {
                "big_tasks": final_state["task_ideas"]
            }
            
        except Exception as e:
            self.logger.error(f"LangGraph 태스크 생성 실패: {str(e)}")
            raise 