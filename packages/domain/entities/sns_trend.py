"""SNS 트렌드 정보를 위한 도메인 엔티티."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from packages.domain.entities.base import Base


class SNSTrend(Base):
    """SNS 트렌드 정보 테이블."""
    
    __tablename__ = "sns_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID, unique=True, nullable=False)  # 실제 테이블에 있는 uuid 필드
    platform = Column(String(50), nullable=False, index=True)  # instagram, tiktok, youtube, twitter 등
    trend_type = Column(String(50), nullable=False, index=True)  # hashtag, challenge, content, legal 등
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    url = Column(String(1000), nullable=True)
    tags = Column(JSON, nullable=True)  # 해시태그, 키워드 등
    engagement_metrics = Column(JSON, nullable=True)  # 좋아요, 댓글, 공유 수 등
    legal_implications = Column(Text, nullable=True)  # 법적 동향 정보
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class TrendEmbedding(Base):
    """트렌드 정보의 벡터 임베딩 테이블."""
    
    __tablename__ = "trend_embeddings"
    
    id = Column(Integer, primary_key=True, index=True)
    trend_uuid = Column(UUID, nullable=False, index=True)  # sns_trends.uuid 참조
    embedding = Column(Text, nullable=False)  # pgvector의 vector 타입 (실제로는 Text로 저장)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
