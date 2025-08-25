"""미션 단계 생성을 위한 LangGraph 노드."""

from typing import Dict, Any
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.logging import get_logger
from packages.infrastructure.prompts.mission_step_prompts import MissionStepPrompts
from packages.presentation.api.dto.response.ai_response_models import MissionStepsAIResponse


class MissionStepGenerationNode:
    """미션 단계 생성을 위한 LangGraph 노드."""
    
    def __init__(self):
        """노드 초기화."""
        self.settings = get_settings()
        self.logger = get_logger("MissionStepGenerationNode")
        
        # Output Parser 설정
        self.output_parser = PydanticOutputParser(pydantic_object=MissionStepsAIResponse)
        
        # LLM 설정
        self.llm = ChatOpenAI(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.7
        )
        
        # 프롬프트 템플릿
        self.prompt_templates = MissionStepPrompts()
    
    async def generate_mission_steps(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """미션 단계를 생성합니다."""
        try:
            # 프롬프트 생성
            prompt = self.prompt_templates.create_prompt_template(
                mission_info=request_data.get("mission_info", ""),
                user_context=request_data.get("user_context", "")
            )
            
            # Chain 구성 및 실행
            chain = prompt | self.llm | self.output_parser
            
            result = chain.invoke({
                "mission_info": request_data.get("mission_info", ""),
                "user_context": request_data.get("user_context", "")
            })
            
            self.logger.info(f"미션 단계 생성 완료: {len(result.mission_steps)}개")
            return result.model_dump()
            
        except Exception as e:
            self.logger.error(f"미션 단계 생성 중 오류: {str(e)}")
            raise
    
    async def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """노드 실행."""
        request_data = state.get("request_data", {})
        result = await self.generate_mission_steps(request_data)
        
        # AI 결과를 상태에 저장하고, 저장 노드에서 사용할 수 있도록 준비
        return {
            **state,
            "ai_result": result,
            "generated_mission_steps": result,
            "mission_id": request_data.get("mission_id")  # mission_id를 상태에 추가
        }
