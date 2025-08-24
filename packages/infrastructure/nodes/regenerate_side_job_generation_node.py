"""사이드잡 재생성을 위한 LangGraph 노드."""

from typing import Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.logging import get_logger
from packages.infrastructure.prompts.regenerate_side_job_prompts import RegenerateSideJobPrompts
from packages.presentation.api.dto.response.ai_response_models import SideJobsAIResponse


class RegenerateSideJobGenerationNode:
    """사이드잡 재생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        """노드 초기화."""
        self.settings = get_settings()
        self.logger = get_logger("RegenerateSideJobGenerationNode")
        
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
        self.prompt_templates = RegenerateSideJobPrompts()
    
    async def regenerate_side_jobs(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """피드백을 바탕으로 사이드잡을 재생성합니다."""
        try:
            generate_request = request_data.get("generateSideJobRequest", {})
            feedback_data = request_data.get("feedbackData", {})
            
            job = generate_request.get("job", "")
            hobbies = generate_request.get("hobbies", [])
            expression_style = generate_request.get("expressionStyle", "글")
            strength_type = generate_request.get("strengthType", "창작")
            
            feedback_reasons = [reason.value for reason in feedback_data.get("reasons", [])]
            etc_feedback = feedback_data.get("etcFeedback")
            
            # 프롬프트 생성
            prompt = self.prompt_templates.create_prompt_template(
                job=job,
                hobbies=hobbies,
                expression_style=expression_style,
                strength_type=strength_type,
                feedback_reasons=feedback_reasons,
                etc_feedback=etc_feedback
            )
            
            # Chain 구성 및 실행
            chain = prompt | self.llm | self.output_parser
            
            result = chain.invoke({
                "job": job,
                "hobbies": hobbies,
                "expression_style": expression_style,
                "strength_type": strength_type,
                "feedback_reasons": feedback_reasons,
                "etc_feedback": etc_feedback
            })
            
            self.logger.info(f"사이드잡 재생성 완료: {len(result.side_jobs)}개")
            return result.model_dump()
            
        except Exception as e:
            self.logger.error(f"사이드잡 재생성 중 오류: {str(e)}")
            raise
    
    async def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """노드 실행."""
        request_data = state.get("request_data", {})
        result = await self.regenerate_side_jobs(request_data)
        
        # AI 결과를 상태에 저장하고, 저장 노드에서 사용할 수 있도록 준비
        return {
            **state,
            "ai_result": result,
            "regenerated_side_jobs": result
        }
