import json
from typing import Dict, List, Any, TypedDict
from langgraph.graph import StateGraph, END
from app.adapters.input.dto.generate_mission_response import GenerateMissionReponse
from app.application.ports.output.generate_mission_output_port import GenerateMissionOutputPort
from app.domain.entities.mission_draft import MissionDraft
from app.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings
from app.infrastructure.services.utils.ai_config_factory import AIConfigFactory
from app.infrastructure.services.utils.ai_response_reader import AIResponseReader

class MissionTaskState(TypedDict):
    messages: Dict[str, str]
    mission_request: GenerateMissionRequest
    generated_missions: List[MissionDraft]

class LangGraphMissionAdapter(GenerateMissionOutputPort):
    def __init__(self):
        self.logger = get_logger("LangGraphMissionAdapter")
        self.settings = get_settings()
        self.ai_config_factory = AIConfigFactory()
        self.response_reader = AIResponseReader()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(MissionTaskState)
        
        workflow.add_node("generate_missions", self._generate_missions)
        workflow.set_entry_point("generate_missions")
        workflow.add_edge("generate_missions", END)
        
        return workflow.compile()
    
    async def _generate_missions(self, state: MissionTaskState) -> MissionTaskState:
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.settings.clova_x_api_key,
                base_url=self.settings.clova_x_base_url
            )
            
            # AI 설정 생성
            model_config = self.ai_config_factory.create_ai_config(
                self.settings.clova_x_provider,
                self.settings.clova_x_model
            )
            
            # API 호출 파라미터 준비
            api_params = {
                "model": model_config.model,
                "messages": [state["messages"]],
                "temperature": model_config.temperature,
                "top_p": model_config.top_p,
                "stream": model_config.streaming
            }
            
            # max_tokens가 None이 아닌 경우에만 추가
            if model_config.max_tokens is not None:
                api_params["max_tokens"] = model_config.max_tokens
            
            # 응답 받기
            response = client.chat.completions.create(**api_params)
            
            # AIResponseReader의 공통 기능을 사용하여 응답 처리
            response_content = self.response_reader.read_ai_response(
                response, 
                is_streaming=model_config.streaming
            )

             # 스트리밍이면 조립 검증
            if model_config.streaming and not self.response_reader.is_brace_balanced(response_content):
                self.logger.warning("JSON brace not balanced; trying repair once.")

            # 1차: 관용 파싱
            try:
                parsed_data = self.response_reader.parse_json_safely(response_content, self.logger)
                state["generated_missions"] = parsed_data.get("result", []) if isinstance(parsed_data, dict) else []
                return state
            except Exception as e:
                self.logger.warning(f"Parse fail; try LLM repair once. err={e}")
            
        except openai.APIConnectionError as e:
            self.logger.error(f"Clova API 연결 오류: {str(e)}")
            state["generated_missions"] = []
            return state
        except Exception as e:
            self.logger.error(f"미션 생성 실패: {str(e)}")
            state["generated_missions"] = []
            return state

    
    async def generate_missions(
        self, 
        messages: Dict[str, str],
        request: GenerateMissionRequest
    ) -> List[MissionDraft]:
        try:
            initial_state = MissionTaskState(
                messages=messages,
                mission_request=request,
                generated_missions=[]
            )
            
            final_state = await self.workflow.ainvoke(initial_state)
            missions = final_state["generated_missions"]

            if not missions:
                raise ValueError("AI 응답에서 미션 리스트가 비어 있습니다.")
            
            return GenerateMissionReponse(
                success=True,
                message="미션 생성 완료",
                tasks=[MissionDraft(**item) for item in missions]
            )
            
        except Exception as e:
            self.logger.error(f"LangGraph 미션 생성 실패: {str(e)}")
            raise
