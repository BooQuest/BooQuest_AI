"""트렌드 검색을 위한 LangGraph 노드."""

from typing import Dict, Union, List
from packages.infrastructure.nodes.base_node import BaseNode
from packages.infrastructure.nodes.states.langgraph_state import SideJobState
from packages.infrastructure.services.trend_retriever_service import TrendRetrieverService


class TrendRetrievalNode(BaseNode[SideJobState]):
    """트렌드 검색을 위한 LangGraph 노드."""
    
    def __init__(self):
        super().__init__("retrieve_trends")
        self.trend_retriever = TrendRetrieverService()
    
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
        """검색 쿼리 기반 관련 트렌드 검색."""
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
        
        return unique_trends[:10]  # 최대 10개 트렌드 반환
    
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
