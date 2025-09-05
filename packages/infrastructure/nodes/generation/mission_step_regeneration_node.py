"""미션 스텝 생성을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.prompts.mission_step_regenerate_prompts import MissionStepRegeneratePrompts
from packages.presentation.api.dto.response.ai_response_models import MissionStepsAIResponse
from langchain_naver import ChatClovaX
from packages.infrastructure.nodes.states.langgraph_state import RegenerateMissionStepState

class MissionStepRegenerationNode(BaseGenerationNode[RegenerateMissionStepState]):
    """미션 스텝 재생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        super().__init__("generate_mission_steps")
        self.settings = get_settings()
        
        # LLM 설정
        self.llm = ChatClovaX(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.7,
            max_tokens=1024,  # Set max tokens larger than 1024 to use tool calling
            thinking={
                "effort": "none"  # Set to "none" to disable thinking, as structured outputs are incompatible with thinking
            },
        )
        
        self.llm = self.llm.with_structured_output(MissionStepsAIResponse, method="json_schema")
        
        # 프롬프트 템플릿
        self.prompt_templates = MissionStepRegeneratePrompts()
    
    async def __call__(self, state: RegenerateMissionStepState) -> RegenerateMissionStepState:
        """노드 실행."""
        try:
            
            # 프롬프트 데이터 준비
            prompt_data = self._prepare_prompt_data(state)

            # 프롬프트 생성 및 format_instructions 적용
            prompt = self.prompt_templates.create_prompt_template()

            # Chain 구성 및 실행
            chain = prompt | self.llm
            result = await chain.ainvoke(prompt_data)

            self.logger.info(f"미션 스텝 생성 완료: {len(result.mission_steps)}개")

            # 공통 상태 업데이트 메서드 사용
            return self._update_generation_state(state, result)
            
        except Exception as e:
            self.logger.error(f"미션 스텝 생성 중 오류: {str(e)}")
            raise
    
    def _prepare_prompt_data(self, state: RegenerateMissionStepState) -> Dict[str, Union[str, List[str]]]:
        """프롬프트 데이터 준비."""
        request_data = self._safe_get(state, "request_data", {})

        return {
            "mission_title": request_data.get("mission_title", "미션 제목"),
            "mission_description": request_data.get("mission_design_notes", "미션 설명"),
            "feedback_reasons": ", ".join(state.get("reasons") or []),
            "etc_feedback": state.get("etc_feedback", ""),
            "order_no": request_data.get("order_no", "0"),
            "side_job_title": request_data.get("side_job_title", "사이드잡 제목"),
            "side_job_description": request_data.get("side_job_description", "사이드잡 설명")
        }
