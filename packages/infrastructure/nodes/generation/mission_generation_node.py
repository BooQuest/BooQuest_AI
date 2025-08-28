"""미션 생성을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.prompts.mission_prompts import MissionPrompts
from packages.presentation.api.dto.response.ai_response_models import MissionsAIResponse
from packages.infrastructure.nodes.states.langgraph_state import MissionState
from langchain_naver import ChatClovaX


class MissionGenerationNode(BaseGenerationNode[MissionState]):
    """미션 생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        super().__init__("generate_missions")
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
        
        # Structured Output 설정
        self.llm = self.llm.with_structured_output(MissionsAIResponse, method="json_schema")
        
        # 프롬프트 템플릿
        self.prompt_templates = MissionPrompts()
    
    def __call__(self, state: MissionState) -> MissionState:
        """노드 실행."""
        try:
            # 프롬프트 데이터 준비
            prompt_data = self._prepare_prompt_data(state)
            
            # 프롬프트 생성
            prompt = self.prompt_templates.create_prompt_template()
            
            # Chain 구성 및 실행
            chain = prompt | self.llm
            result = chain.invoke(prompt_data)
            
            self.logger.info(f"미션 생성 완료: {len(result.missions)}개")
            
            # 공통 상태 업데이트 메서드 사용
            updated_state = self._update_generation_state(state, result)
            
            return updated_state
            
        except Exception as e:
            self.logger.error(f"미션 생성 중 오류: {str(e)}")
            raise
    
    def _prepare_prompt_data(self, state: MissionState) -> Dict[str, Union[str, List[str]]]:
        """프롬프트 데이터 준비."""
        request_data = self._safe_get(state, "request_data", {})
        
        return {
            "side_job_title": request_data.get("side_job_title", "사이드잡 제목"),
            "side_job_description": request_data.get("side_job_description", "사이드잡 설명")
        }