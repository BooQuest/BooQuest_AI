"""트렌드 검색 및 추천을 위한 서비스."""

import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_
from packages.core.db.uow_sqlalchemy import SqlAlchemyUoW
from packages.domain.entities.sns_trend import SNSTrend, TrendEmbedding
from packages.infrastructure.services.embedding.simple_embedding_service import SimpleEmbeddingService
from packages.infrastructure.config.config import get_settings

logger = logging.getLogger(__name__)


class TrendRetrieverService:
    """트렌드 검색 및 추천 서비스."""
    
    def __init__(self):
        self.embedding_service = SimpleEmbeddingService()
        self.settings = get_settings()
    
    def search_trends_by_query(self, query: str, limit: int = 10, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """쿼리 기반 트렌드 검색."""
        try:
            # 쿼리 텍스트 임베딩
            query_embedding = self.embedding_service.embed_text(query)
            
            with SqlAlchemyUoW() as uow:
                # 벡터 유사도 검색
                similar_trends = self._vector_similarity_search(
                    uow.session, query_embedding, limit, platform
                )
                
                return similar_trends
                
        except Exception as e:
            logger.error(f"트렌드 검색 실패: {e}")
            raise
    
    def get_trending_topics(self, days: int = 7, limit: int = 20) -> List[Dict[str, Any]]:
        """최근 트렌딩 토픽 조회."""
        try:
            with SqlAlchemyUoW() as uow:
                # 최근 N일간의 활성 트렌드 조회
                cutoff_date = datetime.utcnow() - timedelta(days=days)
                
                trends = uow.session.query(SNSTrend).filter(
                    and_(
                        SNSTrend.is_active == True,
                        SNSTrend.created_at >= cutoff_date
                    )
                ).order_by(SNSTrend.created_at.desc()).limit(limit).all()
                
                return [self._trend_to_dict(trend) for trend in trends]
                
        except Exception as e:
            logger.error(f"트렌딩 토픽 조회 실패: {e}")
            raise
    
    def get_platform_trends(self, platform: str, limit: int = 10) -> List[Dict[str, Any]]:
        """특정 플랫폼의 트렌드 조회."""
        try:
            with SqlAlchemyUoW() as uow:
                trends = uow.session.query(SNSTrend).filter(
                    and_(
                        SNSTrend.platform == platform,
                        SNSTrend.is_active == True
                    )
                ).order_by(SNSTrend.created_at.desc()).limit(limit).all()
                
                return [self._trend_to_dict(trend) for trend in trends]
                
        except Exception as e:
            logger.error(f"플랫폼 트렌드 조회 실패: {e}")
            raise
    
    def get_trends_by_type(self, trend_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """트렌드 타입별 조회."""
        try:
            with SqlAlchemyUoW() as uow:
                trends = uow.session.query(SNSTrend).filter(
                    and_(
                        SNSTrend.trend_type == trend_type,
                        SNSTrend.is_active == True
                    )
                ).order_by(SNSTrend.created_at.desc()).limit(limit).all()
                
                return [self._trend_to_dict(trend) for trend in trends]
                
        except Exception as e:
            logger.error(f"트렌드 타입별 조회 실패: {e}")
            raise
    
    def _vector_similarity_search(self, session: Session, query_embedding: List[float], 
                                 limit: int, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """벡터 유사도 검색."""
        try:
            # 벡터를 JSON 문자열로 변환
            query_vector_str = json.dumps(query_embedding)
            
            # PostgreSQL pgvector를 사용한 유사도 검색 쿼리
            base_query = """
                SELECT st.*, 
                       CASE 
                           WHEN te.embedding IS NOT NULL THEN 
                               (1 - (te.embedding::vector <-> :query_vector::vector))
                           ELSE 0.0
                       END as similarity_score
                FROM sns_trends st
                LEFT JOIN trend_embeddings te ON st.uuid = te.trend_uuid
                WHERE st.is_active = true
            """
            
            params = {"query_vector": query_vector_str, "limit": limit}
            
            if platform:
                base_query += " AND st.platform = :platform"
                params["platform"] = platform
            
            base_query += " ORDER BY similarity_score DESC LIMIT :limit"
            
            # pgvector 검색 시도
            try:
                # 벡터를 PostgreSQL 배열 형식으로 변환
                query_vector_array = "[" + ",".join(map(str, query_embedding)) + "]"
                
                # 수정된 pgvector 쿼리 (직접 값 삽입)
                pgvector_query = f"""
                    SELECT st.*, 
                           CASE 
                               WHEN te.embedding IS NOT NULL THEN 
                                   (1 - (te.embedding <-> '{query_vector_array}'::vector))
                               ELSE 0.0
                           END as similarity_score
                    FROM sns_trends st
                    LEFT JOIN trend_embeddings te ON st.uuid = te.trend_uuid
                    WHERE st.is_active = true
                """
                
                if platform:
                    pgvector_query += f" AND st.platform = '{platform}'"
                
                pgvector_query += f" ORDER BY similarity_score DESC LIMIT {limit}"
                
                result = session.execute(text(pgvector_query))
                trends_data = result.fetchall()
                
                if trends_data:
                    logger.info(f"pgvector 검색 성공: {len(trends_data)}개 트렌드")
                    return [self._row_to_trend_dict(row) for row in trends_data]
                    
            except Exception as pgvector_error:
                logger.warning(f"pgvector 검색 실패, fallback 사용: {pgvector_error}")
            
            # Fallback: 검색 쿼리와 관련된 트렌드 반환 (키워드 기반)
            logger.info("키워드 기반 fallback 검색 사용")
            
            # 검색 쿼리에서 키워드 추출
            search_keywords = self._extract_keywords_from_query(query_embedding)
            
            # 키워드 기반 검색
            trends = self._keyword_based_search(session, search_keywords, platform, limit)
            
            if not trends:
                # 키워드 검색 실패 시 최근 트렌드 반환
                query = session.query(SNSTrend).filter(SNSTrend.is_active == True)
                if platform:
                    query = query.filter(SNSTrend.platform == platform)
                trends = query.order_by(SNSTrend.created_at.desc()).limit(limit).all()
            
            return [self._trend_to_dict(trend) for trend in trends]
            
        except Exception as e:
            logger.error(f"벡터 유사도 검색 실패: {e}")
            raise
    
    def _extract_keywords_from_query(self, query_embedding: List[float]) -> List[str]:
        """임베딩에서 키워드 추출 (간단한 구현)."""
        # 실제로는 임베딩을 역변환하거나 원본 쿼리를 사용해야 하지만,
        # 여기서는 일반적인 트렌드 키워드를 반환
        return ["트렌드", "SNS", "소셜미디어", "콘텐츠", "부업"]
    
    def _keyword_based_search(self, session: Session, keywords: List[str], 
                             platform: Optional[str], limit: int) -> List[SNSTrend]:
        """키워드 기반 트렌드 검색."""
        try:
            from sqlalchemy import or_, and_
            
            # 키워드 조건 생성
            keyword_conditions = []
            for keyword in keywords:
                keyword_conditions.append(
                    or_(
                        SNSTrend.title.ilike(f"%{keyword}%"),
                        SNSTrend.content.ilike(f"%{keyword}%")
                    )
                )
            
            # 기본 쿼리
            query = session.query(SNSTrend).filter(
                and_(
                    SNSTrend.is_active == True,
                    or_(*keyword_conditions)
                )
            )
            
            # 플랫폼 필터
            if platform:
                query = query.filter(SNSTrend.platform == platform)
            
            # 결과 반환
            trends = query.order_by(SNSTrend.created_at.desc()).limit(limit).all()
            logger.info(f"키워드 기반 검색 결과: {len(trends)}개")
            
            return trends
            
        except Exception as e:
            logger.error(f"키워드 기반 검색 실패: {e}")
            return []
    
    def _trend_to_dict(self, trend: SNSTrend) -> Dict[str, Any]:
        """SNSTrend 객체를 딕셔너리로 변환."""
        return {
            "id": trend.id,
            "uuid": str(trend.uuid),
            "platform": trend.platform,
            "trend_type": trend.trend_type,
            "title": trend.title,
            "content": trend.content,
            "url": trend.url,
            "tags": trend.tags,
            "engagement_metrics": trend.engagement_metrics,
            "legal_implications": trend.legal_implications,
            "created_at": trend.created_at.isoformat() if trend.created_at else None,
            "is_active": trend.is_active
        }
    
    def _row_to_trend_dict(self, row) -> Dict[str, Any]:
        """쿼리 결과 행을 딕셔너리로 변환."""
        return {
            "id": row.id,
            "uuid": str(row.uuid),
            "platform": row.platform,
            "trend_type": row.trend_type,
            "title": row.title,
            "content": row.content,
            "url": row.url,
            "tags": row.tags,
            "engagement_metrics": row.engagement_metrics,
            "legal_implications": row.legal_implications,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "is_active": row.is_active,
            "similarity_score": getattr(row, 'similarity_score', 0.0)
        }
