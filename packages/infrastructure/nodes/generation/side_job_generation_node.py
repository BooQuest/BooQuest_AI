"""사이드잡 생성을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.nodes.base_node import BaseGenerationNode
from packages.infrastructure.prompts.side_job_prompts import SideJobPrompts
from packages.presentation.api.dto.response.ai_response_models import SideJobsAIResponse
from packages.infrastructure.nodes.states.langgraph_state import SideJobState
from langchain_naver import ChatClovaX


class SideJobGenerationNode(BaseGenerationNode[SideJobState]):
    """사이드잡 생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        super().__init__("generate_side_jobs")
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
        self.llm = self.llm.with_structured_output(SideJobsAIResponse, method="json_schema")
        
        # 프롬프트 템플릿
        self.prompt_templates = SideJobPrompts()
    
    def __call__(self, state: SideJobState) -> SideJobState:
        """노드 실행."""
        try:
            # 프롬프트 데이터 준비
            prompt_data = self._prepare_prompt_data(state)
            
            # 프롬프트 생성
            prompt = self.prompt_templates.create_prompt_template()
            self.logger.info(f"프롬프트: {prompt.format(**prompt_data)}")

            # Chain 구성 및 실행
            chain = prompt | self.llm
            result = chain.invoke(prompt_data)
            
            self.logger.info(f"사이드잡 생성 완료: {len(result.side_jobs)}개")
            
            # 공통 상태 업데이트 메서드 사용
            updated_state = self._update_generation_state(state, result)
            
            return updated_state
            
        except Exception as e:
            self.logger.error(f"사이드잡 생성 중 오류: {str(e)}")
            raise
    
    def _prepare_prompt_data(self, state: SideJobState) -> Dict[str, Union[str, List[str]]]:
        """프롬프트 데이터 준비."""
        profile_data = self._safe_get(state, "profile_data", {})
        expression_style = profile_data.get("expression_style", "")
        # 플랫폼 데이터 로더에서 데이터 가져오기
        expression_jobs = self.prompt_templates.platform_loader.get_expression_side_jobs(expression_style)
        platform_list = expression_jobs.get(expression_style.upper(), [])  # ← 중요

        platform_names = ", ".join(platform_list)
        self.logger.info(f"[✅ platform_names]: {platform_names}")
        return {
            "job": profile_data.get("job", ""),
            "hobbies": ", ".join(profile_data.get("hobbies", [])),
            "expression_style": expression_style,
            "strength_type": profile_data.get("strength_type", ""),
            "platform_names": platform_names
        }
    
