"""트렌드 데이터 저장 및 관리 서비스."""

import logging
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from packages.core.db.uow_sqlalchemy import SqlAlchemyUoW
from packages.domain.entities.sns_trend import SNSTrend, TrendEmbedding
from packages.infrastructure.services.embedding.simple_embedding_service import SimpleEmbeddingService

logger = logging.getLogger(__name__)


class TrendStorageService:
    """트렌드 데이터 저장 및 관리 서비스."""
    
    def __init__(self):
        self.embedding_service = SimpleEmbeddingService()
    
    def save_trends(self, trends: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """트렌드 데이터를 저장하고 임베딩을 생성 (개별 트랜잭션 사용)."""
        saved_trends = []
        
        for trend_data in trends:
            try:
                # 각 트렌드별로 개별 트랜잭션 사용
                with SqlAlchemyUoW() as uow:
                    # 트렌드 저장
                    saved_trend = self._save_trend(uow.session, trend_data)
                    
                    # None 값 체크
                    if saved_trend is None:
                        logger.warning(f"트렌드 저장 실패 (None 반환): {trend_data}")
                        continue
                    
                    # 임베딩 생성 및 저장
                    self._save_embedding(uow.session, saved_trend)
                    
                    saved_trends.append(saved_trend)
                    logger.info(f"트렌드 저장 성공: {saved_trend.get('title', 'N/A')}")
                    
            except Exception as e:
                logger.error(f"개별 트렌드 저장 실패: {e}")
                continue
        
        logger.info(f"트렌드 저장 완료: {len(saved_trends)}개")
        return saved_trends
    
    def _is_duplicate_trend(self, session: Session, trend_data: Dict[str, Any]) -> bool:
        """중복 트렌드 체크."""
        try:
            # 제목과 플랫폼을 안전하게 처리
            title = trend_data.get("title", "")
            platform = trend_data.get("platform", "")
            
            # UTF-8 인코딩 문제 해결
            if isinstance(title, bytes):
                title = title.decode('utf-8', errors='ignore')
            if isinstance(platform, bytes):
                platform = platform.decode('utf-8', errors='ignore')
            
            # 제목과 플랫폼으로 중복 체크
            existing = session.query(SNSTrend).filter(
                SNSTrend.title == title,
                SNSTrend.platform == platform
            ).first()
            
            return existing is not None
            
        except Exception as e:
            logger.error(f"중복 체크 실패: {e}")
            return False
    
    def _save_trend(self, session: Session, trend_data: Dict[str, Any]) -> Dict[str, Any]:
        """트렌드 데이터 저장 (직접 SQL 사용)."""
        try:
            # 데이터 형식 확인 및 변환
            if isinstance(trend_data, str):
                logger.error(f"trend_data가 문자열입니다: {trend_data}")
                return None
            
            # 데이터를 안전하게 처리
            def safe_decode(value):
                if isinstance(value, bytes):
                    return value.decode('utf-8', errors='ignore')
                elif isinstance(value, str):
                    # 문자열도 UTF-8로 재인코딩/디코딩하여 문제 문자 제거
                    try:
                        return value.encode('utf-8', errors='ignore').decode('utf-8')
                    except:
                        return str(value)
                return str(value) if value else ''
            
            import uuid
            import json
            
            # UUID 생성
            trend_uuid = str(uuid.uuid4())
            
            # SQLAlchemy Core insert 사용 (기존 프로젝트 패턴)
            insert_data = {
                "uuid": trend_uuid,
                "platform": safe_decode(trend_data.get("platform")),
                "trend_type": safe_decode(trend_data.get("trend_type")),
                "title": safe_decode(trend_data.get("title")),
                "content": safe_decode(trend_data.get("content")),
                "url": safe_decode(trend_data.get("url")),
                "tags": json.dumps(trend_data.get("tags", [])),
                "engagement_metrics": json.dumps(trend_data.get("engagement_metrics", {})),
                "legal_implications": safe_decode(trend_data.get("legal_implications")),
                "created_at": trend_data.get("created_at", datetime.utcnow())
            }
            
            # SNSTrend 테이블에 삽입
            from sqlalchemy import insert
            stmt = insert(SNSTrend.__table__).values(insert_data).returning(SNSTrend.__table__.c.id)
            result = session.execute(stmt)
            trend_id = result.fetchone()[0]
            
            # 딕셔너리로 변환하여 반환
            saved_trend = {
                "id": trend_id,
                "uuid": trend_uuid,
                "platform": safe_decode(trend_data.get("platform")),
                "trend_type": safe_decode(trend_data.get("trend_type")),
                "title": safe_decode(trend_data.get("title")),
                "content": safe_decode(trend_data.get("content")),
                "url": safe_decode(trend_data.get("url")),
                "tags": trend_data.get("tags"),
                "engagement_metrics": trend_data.get("engagement_metrics"),
                "legal_implications": safe_decode(trend_data.get("legal_implications")),
                "created_at": trend_data.get("created_at", datetime.utcnow())
            }
            
            return saved_trend
            
        except Exception as e:
            logger.error(f"트렌드 저장 실패: {e}")
            raise
    
    def _save_embedding(self, session: Session, trend_data: Dict[str, Any]):
        """트렌드 임베딩 저장 (직접 SQL 사용)."""
        try:
            # 임베딩 생성
            text = f"{trend_data.get('title', '')} {trend_data.get('content', '')}"
            embedding_vector = self.embedding_service.embed_text(text)
            
            # 벡터를 문자열로 변환 (pgvector 형식)
            import json
            vector_str = json.dumps(embedding_vector)
            
            # SQLAlchemy Core insert 사용 (기존 프로젝트 패턴)
            from sqlalchemy import insert
            insert_data = {
                "trend_uuid": trend_data["uuid"],
                "embedding": vector_str,
                "created_at": datetime.utcnow()
            }
            
            stmt = insert(TrendEmbedding.__table__).values(insert_data)
            session.execute(stmt)
            
        except Exception as e:
            logger.error(f"임베딩 저장 실패: {e}")
            raise
    
    def search_similar_trends(self, query_text: str, limit: int = 10) -> List[Dict[str, Any]]:
        """유사한 트렌드 검색."""
        try:
            # 쿼리 텍스트 임베딩
            query_embedding = self.embedding_service.embed_text(query_text)
            
            with SqlAlchemyUoW() as uow:
                # 벡터 유사도 검색 (PostgreSQL pgvector 사용)
                # 실제 구현에서는 SQL 쿼리로 벡터 유사도 검색을 수행
                similar_trends = self._vector_search(uow.session, query_embedding, limit)
                
                return similar_trends
                
        except Exception as e:
            logger.error(f"유사 트렌드 검색 실패: {e}")
            raise
    
    def _vector_search(self, session: Session, query_embedding: List[float], limit: int) -> List[Dict[str, Any]]:
        """벡터 유사도 검색."""
        try:
            # PostgreSQL pgvector를 사용한 유사도 검색
            # 실제 구현에서는 SQL 쿼리로 수행
            # 예시: SELECT * FROM sns_trends st 
            #       JOIN trend_embeddings te ON st.id = te.trend_id 
            #       ORDER BY te.embedding_vector <-> %s LIMIT %s
            
            # 여기서는 간단한 예시로 최근 트렌드 반환
            trends = session.query(SNSTrend).order_by(SNSTrend.created_at.desc()).limit(limit).all()
            
            result = []
            for trend in trends:
                result.append({
                    "id": trend.id,
                    "platform": trend.platform,
                    "trend_type": trend.trend_type,
                    "title": trend.title,
                    "content": trend.content,
                    "url": trend.url,
                    "tags": trend.tags,
                    "engagement_metrics": trend.engagement_metrics,
                    "legal_implications": trend.legal_implications,
                    "created_at": trend.created_at
                })
            
            return result
            
        except Exception as e:
            logger.error(f"벡터 검색 실패: {e}")
            raise
