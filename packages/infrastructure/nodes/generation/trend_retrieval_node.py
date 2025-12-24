"""트렌드 검색을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from packages.infrastructure.nodes.base_node import BaseNode
from packages.infrastructure.nodes.states.langgraph_state import SideJobState
from packages.infrastructure.services.trend_retriever_service import TrendRetrieverService
from packages.infrastructure.config.config import get_settings
from packages.infrastructure.prompts.trend_validation_prompts import TrendValidationPrompts
from packages.presentation.api.dto.response.ai_response_models import TrendValidationResponse
from langchain_naver import ChatClovaX


class TrendRetrievalNode(BaseNode[SideJobState]):
    """트렌드 검색을 위한 LangGraph 노드."""
    
    def __init__(self):
        super().__init__("retrieve_trends")
        self.trend_retriever = TrendRetrieverService()
        self.settings = get_settings()
        
        # 트렌드 검증용 LLM 설정
        self.validation_llm = ChatClovaX(
            api_key=self.settings.clova_x_api_key,
            base_url=self.settings.clova_x_base_url,
            model=self.settings.clova_x_model,
            temperature=0.3,  # 검증은 낮은 temperature 사용
            max_tokens=512,
            thinking={
                "effort": "none"
            },
        )
        
        # Structured Output 설정
        self.validation_llm = self.validation_llm.with_structured_output(
            TrendValidationResponse, method="json_schema"
        )
        
        # 검증 프롬프트 템플릿
        self.validation_prompts = TrendValidationPrompts()
    
    def __call__(self, state: SideJobState) -> SideJobState:
        """노드 실행."""
        self.logger.info("TrendRetrievalNode 실행 시작")
        
        try:
            # 중첩된 profile_data 구조 처리
            raw_profile_data = self._safe_get(state, "profile_data", {})
            
            # profile_data가 중첩되어 있는 경우 처리
            if "profile_data" in raw_profile_data:
                profile_data = raw_profile_data["profile_data"]
            else:
                profile_data = raw_profile_data
            
            # 트렌드 검색 쿼리 생성
            search_queries = self._create_search_queries(profile_data)
            
            # 트렌드 검색 실행
            relevant_trends = self._search_relevant_trends(search_queries)
            
            # 상태 업데이트 (완전히 새로운 상태 객체 생성)
            trend_data = {
                "search_queries": search_queries,
                "relevant_trends": relevant_trends,
                "trend_summary": self._create_trend_summary(relevant_trends)
            }
            
            # 기존 상태를 복사하고 trend_data 추가
            updated_state = {
                "user_id": state.get("user_id"),
                "ai_result": state.get("ai_result"),
                "saved_entities": state.get("saved_entities"),
                "profile_data": state.get("profile_data"),
                "side_job_ids": state.get("side_job_ids"),
                "trend_data": trend_data
            }
            
            self.logger.info(f"트렌드 검색 완료: {len(relevant_trends)}개 트렌드 발견")
            self.logger.info(f"트렌드 데이터 설정 완료: {len(relevant_trends)}개 트렌드")
            
            return updated_state
            
        except Exception as e:
            self.logger.error(f"트렌드 검색 중 오류: {str(e)}")
            # 오류 발생 시 빈 트렌드 데이터로 계속 진행
            empty_trend_data = {
                "search_queries": [],
                "relevant_trends": [],
                "trend_summary": "트렌드 정보를 가져올 수 없습니다."
            }
            
            # 기존 상태를 복사하고 빈 trend_data 추가
            updated_state = {
                "user_id": state.get("user_id"),
                "ai_result": state.get("ai_result"),
                "saved_entities": state.get("saved_entities"),
                "profile_data": state.get("profile_data"),
                "side_job_ids": state.get("side_job_ids"),
                "trend_data": empty_trend_data
            }
            
            return updated_state
    
    def _create_search_queries(self, profile_data: Dict[str, Union[str, List[str]]]) -> List[str]:
        """사용자 프로필 기반 검색 쿼리 생성."""
        queries = []
        
        # 직업 기반 쿼리
        job = profile_data.get("job", "")
        if job:
            queries.append(f"{job} 관련 최신 트렌드")
            queries.append(f"{job} 부업 아이디어")
        
        # 취미 기반 쿼리
        hobbies = profile_data.get("hobbies", [])
        for hobby in hobbies:
            queries.append(f"{hobby} 관련 트렌드")
            queries.append(f"{hobby}로 수익 창출")
        
        # 표현 스타일 기반 쿼리
        expression_style = profile_data.get("expression_style", "")
        if expression_style:
            queries.append(f"{expression_style} 스타일 콘텐츠 트렌드")
        
        # 강점 타입 기반 쿼리
        strength_type = profile_data.get("strength_type", "")
        if strength_type:
            queries.append(f"{strength_type} 활용 부업")
        
        return queries[:5]  # 최대 5개 쿼리로 제한
    
    def _search_relevant_trends(self, search_queries: List[str]) -> List[Dict[str, any]]:
        """검색 쿼리 기반 관련 트렌드 검색 및 검증."""
        all_trends = []
        
        self.logger.info(f"검색 쿼리 목록: {search_queries}")
        
        for query in search_queries:
            try:
                # 각 쿼리별로 트렌드 검색
                self.logger.info(f"쿼리 '{query}' 검색 시작...")
                trends = self.trend_retriever.search_trends_by_query(query, limit=3)
                self.logger.info(f"쿼리 '{query}' 검색 결과: {len(trends)}개")
                all_trends.extend(trends)
            except Exception as e:
                self.logger.warning(f"쿼리 '{query}' 검색 실패: {e}")
                continue
        
        self.logger.info(f"전체 트렌드 수집: {len(all_trends)}개")
        
        # 중복 제거 및 정렬
        unique_trends = self._deduplicate_trends(all_trends)
        
        self.logger.info(f"중복 제거 후 트렌드: {len(unique_trends)}개")
        
        # AI 검증을 통해 부업 정보로 활용 가능한 트렌드만 필터링
        validated_trends = self._validate_trends(unique_trends)
        
        self.logger.info(f"검증 후 유효한 트렌드: {len(validated_trends)}개")
        
        return validated_trends[:10]  # 최대 10개 트렌드 반환
    
    def _create_trend_summary(self, trends: List[Dict[str, any]]) -> str:
        """트렌드 요약 정보 생성."""
        if not trends:
            return "관련 트렌드 정보가 없습니다."
        
        # 플랫폼별 트렌드 그룹화
        platform_trends = {}
        for trend in trends:
            platform = trend.get("platform", "unknown")
            if platform not in platform_trends:
                platform_trends[platform] = []
            platform_trends[platform].append(trend.get("title", ""))
        
        # 요약 생성
        summary_parts = []
        for platform, trend_titles in platform_trends.items():
            summary_parts.append(f"{platform}: {', '.join(trend_titles[:2])}")
        
        return f"최신 트렌드: {' | '.join(summary_parts)}"
    
    def _deduplicate_trends(self, trends: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """중복 트렌드 제거."""
        seen_uuids = set()
        unique_trends = []
        
        for trend in trends:
            uuid = trend.get("uuid")
            if uuid and uuid not in seen_uuids:
                seen_uuids.add(uuid)
                unique_trends.append(trend)
        
        # 최신순으로 정렬
        unique_trends.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        
        return unique_trends
    
    def _validate_trends(self, trends: List[Dict[str, any]]) -> List[Dict[str, any]]:
        """AI를 사용하여 트렌드가 부업 정보로 활용 가능한지 검증."""
        validated_trends = []
        
        if not trends:
            return validated_trends
        
        self.logger.info(f"트렌드 검증 시작: {len(trends)}개")
        
        for trend in trends:
            try:
                # 트렌드 검증 실행
                is_valid = self._validate_single_trend(trend)
                
                if is_valid:
                    validated_trends.append(trend)
                    self.logger.debug(f"트렌드 검증 통과: {trend.get('title', 'N/A')[:50]}")
                else:
                    self.logger.debug(f"트렌드 검증 실패: {trend.get('title', 'N/A')[:50]}")
                    
            except Exception as e:
                self.logger.warning(f"트렌드 검증 중 오류 발생 (트렌드 제외): {e}")
                # 검증 실패 시 해당 트렌드는 제외 (안전한 선택)
                continue
        
        return validated_trends
    
    def _validate_single_trend(self, trend: Dict[str, any]) -> bool:
        """단일 트렌드 검증."""
        try:
            platform = trend.get("platform", "")
            title = trend.get("title", "")
            content = trend.get("content", "") or title  # content가 없으면 title 사용
            
            # 프롬프트 데이터 준비
            prompt_data = {
                "platform": platform,
                "title": title,
                "content": content[:500]  # 너무 긴 내용은 제한
            }
            
            # 프롬프트 생성 및 실행
            prompt_template = self.validation_prompts.create_validation_prompt_template()
            chain = prompt_template | self.validation_llm
            result = chain.invoke(prompt_data)
            
            # 검증 결과 반환 (Y면 True, N이면 False)
            if hasattr(result, 'validation_result'):
                return result.validation_result == "Y"
            return False
            
        except Exception as e:
            self.logger.error(f"트렌드 검증 중 예외 발생: {e}")
            # 검증 실패 시 안전하게 False 반환
            return False
