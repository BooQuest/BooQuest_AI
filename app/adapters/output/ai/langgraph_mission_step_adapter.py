from asyncio import tasks
import json
from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, END
from app.adapters.input.dto.generate_mission_step_response import GenerateMissionStepResponse
from app.application.ports.output.mission_step_generation_output_port import MissionStepGenerationOutputPort
from app.domain.entities.mission_step import MissionStep
from app.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from app.adapters.input.dto.generate_mission_step_response import GenerateMissionStepResponse
from app.infrastructure.logging import get_logger
from app.infrastructure.config import get_settings
from app.infrastructure.services.utils.ai_config_factory import AIConfigFactory
from app.infrastructure.services.utils.ai_response_reader import AIResponseReader

class MissionStepTaskState(TypedDict):
    messages: Dict[str, str]
    mission_step_request: GenerateMissionStepRequest
    generated_steps: List[MissionStep]

class LangGraphMissionStepAdapter(MissionStepGenerationOutputPort):
    def __init__(self):
        self.logger = get_logger("LangGraphMissionStepAdapter")
        self.settings = get_settings()
        self.ai_config_factory = AIConfigFactory()
        self.response_reader = AIResponseReader()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        workflow = StateGraph(MissionStepTaskState)
        
        workflow.add_node("generate_mission_steps", self._generate_mission_steps)
        workflow.set_entry_point("generate_mission_steps")
        workflow.add_edge("generate_mission_steps", END)
        
        return workflow.compile()
    
    async def _generate_mission_steps(self, state: MissionStepTaskState) -> MissionStepTaskState:
        try:
            import openai
            client = openai.OpenAI(
                api_key=self.settings.clova_x_api_key,
                base_url=self.settings.clova_x_base_url
            )
            
            messages = state['messages']
            
            # AI 설정 생성
            model_config = self.ai_config_factory.create_ai_config(
                self.settings.clova_x_provider,
                self.settings.clova_x_model
            )
            
            # API 호출 파라미터 준비
            api_params = {
                "model": model_config.model,
                "messages": [messages],
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
            
            # MissionStep 배열로 파싱
            try:
                from app.domain.entities.mission_step import MissionStep
                
                steps = json.loads(response_content)
                state["generated_steps"] = steps.get("result", []) 
                
            except Exception as e:
                self.logger.error(f"MissionStep 파싱 실패: {str(e)}")
                state["generated_steps"] = []
            
            return state
            
        except openai.APIConnectionError as e:
            self.logger.error(f"Clova API 연결 오류: {str(e)}")
            state["generated_steps"] = []
            return state
        except Exception as e:
            self.logger.error(f"미션 스텝 생성 실패: {str(e)}")
            state["generated_steps"] = []
            return state
    

    
    async def generate_mission_steps(self, messages: Dict[str, str], request: GenerateMissionStepRequest) -> List[MissionStep]:
        try:
            initial_state = MissionStepTaskState(
                messages=messages,
                mission_step_request=request,
                generated_steps=[]
            )
            
            final_state = await self.workflow.ainvoke(initial_state)
            missionSteps = final_state["generated_steps"]
            
            if not missionSteps:
                raise ValueError("AI 응답에서 부퀘스트 리스트가 비어 있습니다.")
            
            return GenerateMissionStepResponse(
                success=True,
                message="미션 생성 완료",
                steps=[MissionStep(**item) for item in missionSteps],
            )
            
        except Exception as e:
            self.logger.error(f"LangGraph 미션 스텝 생성 실패: {str(e)}")
            raise
