"""사이드잡 재생성을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from langchain_core.output_parsers import PydanticOutputParser
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.prompts.regenerate_side_job_prompts import RegenerateSideJobPrompts
from packages.presentation.api.dto.response.ai_response_models import SideJobsAIResponse
from packages.infrastructure.nodes.states.langgraph_state import SideJobState
from langchain_naver import ChatClovaX


class RegenerateSideJobGenerationNode(BaseGenerationNode[SideJobState]):
    """사이드잡 재생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        super().__init__("regenerate_side_jobs")
        self.settings = get_settings()
        
        # LLM 설정
        self.llm = ChatClovaX(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.7
        )
        
        # Output Parser 설정
        self.output_parser = PydanticOutputParser(pydantic_object=SideJobsAIResponse)
        
        # 프롬프트 템플릿
        self.prompt_templates = RegenerateSideJobPrompts()
    
    async def __call__(self, state: SideJobState) -> SideJobState:
        """노드 실행."""
        try:
            # 프롬프트 데이터 준비
            prompt_data = self._prepare_prompt_data(state)
            
            # 프롬프트 생성 및 format_instructions 적용
            prompt = self.prompt_templates.create_prompt_template(**prompt_data).partial(
                format_instructions=self.output_parser.get_format_instructions()
            )
            
            # Chain 구성 및 실행
            chain = prompt | self.llm | self.output_parser
            result = chain.invoke(prompt_data)
            
            self.logger.info(f"사이드잡 재생성 완료: {len(result.side_jobs)}개")
            
            # 공통 상태 업데이트 메서드 사용
            return self._update_generation_state(state, result)
            
        except Exception as e:
            self.logger.error(f"사이드잡 재생성 중 오류: {str(e)}")
            raise
    
    def _prepare_prompt_data(self, state: SideJobState) -> Dict[str, Union[str, List[str]]]:
        """프롬프트 데이터 준비."""
        profile_data = self._safe_get(state, "profile_data", {})
        
        # 기본 프로필 데이터
        prompt_data = {
            "job": profile_data.get("job", ""),
            "hobbies": ", ".join(profile_data.get("hobbies", [])),
            "expression_style": profile_data.get("expressionStyle", "글"),
            "strength_type": profile_data.get("strengthType", "창작")
        }
        
        # 피드백 데이터 추가 (안전하게 처리)
        feedback_reasons = profile_data.get("feedback_reasons", [])
        etc_feedback = profile_data.get("etc_feedback", "")
        
        # feedback_reasons가 리스트인지 확인하고 문자열로 변환
        if isinstance(feedback_reasons, list):
            prompt_data["feedback_reasons"] = ", ".join(feedback_reasons)
        elif isinstance(feedback_reasons, str):
            prompt_data["feedback_reasons"] = feedback_reasons
        else:
            prompt_data["feedback_reasons"] = "피드백 사유가 제공되지 않았습니다"
        
        # etc_feedback 처리
        if etc_feedback:
            prompt_data["etc_feedback"] = etc_feedback
        else:
            prompt_data["etc_feedback"] = "추가 피드백이 없습니다"
        
        return prompt_data
