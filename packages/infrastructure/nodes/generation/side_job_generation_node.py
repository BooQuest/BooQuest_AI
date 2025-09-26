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
        # 상태 로깅
        self.logger.info("SideJobGenerationNode 실행 시작")
        
        # 중첩된 profile_data 구조 처리
        raw_profile_data = self._safe_get(state, "profile_data", {})
        
        # profile_data가 중첩되어 있는 경우 처리
        if "profile_data" in raw_profile_data:
            profile_data = raw_profile_data["profile_data"]
        else:
            profile_data = raw_profile_data
            
        trend_data = self._safe_get(state, "trend_data", {})
        
        # 디버깅 로그 추가
        self.logger.info(f"원본 프로필 데이터: {raw_profile_data}")
        self.logger.info(f"처리된 프로필 데이터: {profile_data}")
        self.logger.info(f"트렌드 데이터: {trend_data}")
        
        expression_style = profile_data.get("expression_style", "")
        
        # 표현 방식 매핑
        style_mapping = {
            "글": "TEXT",
            "그림": "IMAGE", 
            "영상": "VIDEO"
        }
        
        mapped_style = style_mapping.get(expression_style, expression_style.upper())
        
        # 플랫폼 데이터 로더에서 데이터 가져오기
        expression_jobs = self.prompt_templates.platform_loader.get_expression_side_jobs(mapped_style)
        platform_list = expression_jobs.get(mapped_style, [])

        platform_names = ", ".join(platform_list)
        
        # 트렌드 정보 추출
        trend_summary = trend_data.get("trend_summary", "")
        relevant_trends = trend_data.get("relevant_trends", [])
        
        # 트렌드 상세 정보 생성
        trend_details = self._format_trend_details(relevant_trends)
        
        # 디버깅 로그 추가
        self.logger.info(f"플랫폼 목록: {platform_list}")
        self.logger.info(f"트렌드 요약: {trend_summary}")
        self.logger.info(f"관련 트렌드 개수: {len(relevant_trends)}")

        prompt_data = {
            "job": profile_data.get("job", ""),
            "hobbies": ", ".join(profile_data.get("hobbies", [])),
            "expression_style": expression_style,
            "strength_type": profile_data.get("strength_type", ""),
            "platform_names": platform_names,
            "trend_summary": trend_summary,
            "trend_details": trend_details
        }
        
        self.logger.info(f"최종 프롬프트 데이터: {prompt_data}")
        return prompt_data
    
    def _format_trend_details(self, trends: List[Dict[str, any]]) -> str:
        """트렌드 상세 정보 포맷팅."""
        if not trends:
            return "현재 관련 트렌드 정보가 없습니다."
        
        trend_info = []
        for trend in trends[:5]:  # 최대 5개 트렌드만 포함
            platform = trend.get("platform", "")
            title = trend.get("title", "")
            content = trend.get("content", "")[:100] + "..." if len(trend.get("content", "")) > 100 else trend.get("content", "")
            
            trend_info.append(f"• {platform}: {title} - {content}")
        
        return "\n".join(trend_info)
    
