"""SideJob SQLAlchemy Core 모델."""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Index, MetaData, Table
from datetime import datetime

# 메타데이터 생성
metadata = MetaData()

# SideJob 테이블 정의 (Core 방식)
SideJob = Table(
    "side_jobs",
    metadata,
    
    # 컬럼 정의
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),  # 외래키 제약조건 제거
    Column("title", String(255), nullable=False),
    Column("description", Text, nullable=False),
    Column("prompt_meta", Text, nullable=True),
    Column("is_selected", Boolean, default=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    
    
    # 테이블 주석
    comment="AI-generated side jobs for users"
)
