"""사이드잡 생성을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from langchain_core.output_parsers import PydanticOutputParser
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
            temperature=0.7
        )
        
        # Output Parser 설정
        self.output_parser = PydanticOutputParser(pydantic_object=SideJobsAIResponse)
        
        # 프롬프트 템플릿
        self.prompt_templates = SideJobPrompts()
    
    def __call__(self, state: SideJobState) -> SideJobState:
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
        
        # 플랫폼 데이터 로더를 통해 플랫폼 정보 가져오기
        platform_loader = self.prompt_templates.platform_loader
        
        # 플랫폼 이름들
        platform_names = platform_loader.all_platform_names
        platform_names_str = ", ".join([item["name"] for item in platform_names])
        
        # SNS 플랫폼들
        sns_platforms = []
        media_types = platform_loader.get_media_types()
        for media_type, platforms in media_types.items():
            for platform in platforms:
                sns_platforms.append(f"{platform} ({media_type})")
        sns_platforms_str = ", ".join(sns_platforms)
        
        return {
            "job": profile_data.get("job", ""),
            "hobbies": ", ".join(profile_data.get("hobbies", [])),
            "expression_style": profile_data.get("expressionStyle", "글"),
            "strength_type": profile_data.get("strengthType", "창작"),
            "platform_names": platform_names_str,
            "sns_platforms": sns_platforms_str
        }
    
