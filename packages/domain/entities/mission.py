"""Mission SQLAlchemy Core 모델."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Index, MetaData, Table
from datetime import datetime
from .base import MissionStatus

# 메타데이터 생성
metadata = MetaData()

# Mission 테이블 정의 (Core 방식)
Mission = Table(
    "missions",
    metadata,
    
    # 컬럼 정의
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),  # 외래키 제약조건 제거
    Column("sidejob_id", Integer, nullable=True),  # 외래키 제약조건 제거
    Column("title", String(255), nullable=False),
    Column("order_no", Integer, nullable=False),
    Column("design_notes", Text, nullable=True),
    Column("guide", Text, nullable=True),
    Column("status", String(50), default=MissionStatus.PLANNED),
    Column("created_at", DateTime, default=datetime.utcnow),
    
    
    # 테이블 주석
    comment="AI-generated missions for side jobs"
)
