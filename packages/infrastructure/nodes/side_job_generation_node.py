"""사이드잡 생성을 위한 LangGraph 노드."""

from typing import Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.logging import get_logger
from packages.infrastructure.prompts.side_job_prompts import SideJobPrompts
from packages.presentation.api.dto.response.ai_response_models import SideJobsAIResponse


class SideJobGenerationNode:
    """사이드잡 생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        """노드 초기화."""
        self.settings = get_settings()
        self.logger = get_logger("SideJobGenerationNode")
        
        # Output Parser 설정
        self.output_parser = PydanticOutputParser(pydantic_object=SideJobsAIResponse)
        
        # LLM 설정
        self.llm = ChatOpenAI(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.7
        )
        
        # 프롬프트 템플릿
        self.prompt_templates = SideJobPrompts()
    
    async def generate_side_jobs(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """사이드잡을 생성합니다."""
        try:
            # 프롬프트 생성
            prompt = self.prompt_templates.create_prompt_template(
                job=profile_data.get("job", ""),
                hobbies=profile_data.get("hobbies", []),
                expression_style=profile_data.get("expressionStyle", "글"),
                strength_type=profile_data.get("strengthType", "창작")
            )
            
            # Chain 구성 및 실행
            chain = prompt | self.llm | self.output_parser
            
            result = chain.invoke({
                "job": profile_data.get("job", ""),
                "hobbies": profile_data.get("hobbies", []),
                "expression_style": profile_data.get("expressionStyle", "글"),
                "strength_type": profile_data.get("strengthType", "창작")
            })
            
            self.logger.info(f"사이드잡 생성 완료: {len(result.side_jobs)}개")
            return result.model_dump()
            
        except Exception as e:
            self.logger.error(f"사이드잡 생성 중 오류: {str(e)}")
            raise
    
    async def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """노드 실행."""
        profile_data = state.get("profile_data", {})
        result = await self.generate_side_jobs(profile_data)
        
        # AI 결과를 상태에 저장하고, 저장 노드에서 사용할 수 있도록 준비
        return {
            **state,
            "ai_result": result,
            "generated_side_jobs": result,
            "user_id": profile_data.get("user_id")  # user_id를 상태에 추가
        }
