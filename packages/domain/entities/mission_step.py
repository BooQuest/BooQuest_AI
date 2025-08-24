"""MissionStep SQLAlchemy Core 모델."""

from sqlalchemy import Column, Integer, String, Text, DateTime, Index, MetaData, Table
from datetime import datetime
from .base import StepStatus

# 메타데이터 생성
metadata = MetaData()

# MissionStep 테이블 정의 (Core 방식)
MissionStep = Table(
    "mission_steps",
    metadata,
    
    # 컬럼 정의
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("mission_id", Integer, nullable=False),  # 외래키 제약조건 제거
    Column("seq", Integer, nullable=False),
    Column("title", String(255), nullable=False),
    Column("detail", Text, nullable=False),
    Column("status", String(50), default=StepStatus.PLANNED),
    Column("created_at", DateTime, default=datetime.utcnow),
    
    
    # 테이블 주석
    comment="AI-generated mission steps for missions"
)
