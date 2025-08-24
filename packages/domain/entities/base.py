"""공통 Base 클래스와 Enum 정의."""

from sqlalchemy.orm import DeclarativeBase
import enum


class Base(DeclarativeBase):
    """SQLAlchemy ORM Base 클래스.
    
    모든 ORM 모델이 상속받는 기본 클래스입니다.
    DeclarativeBase를 사용하여 최신 SQLAlchemy 2.0 스타일을 따릅니다.
    """
    pass


class StepStatus(str, enum.Enum):
    """미션 단계 상태 Enum.
    
    비즈니스 규칙:
    - PLANNED: 계획된 단계 (기본값)
    - IN_PROGRESS: 진행 중인 단계
    - COMPLETED: 완료된 단계
    - SKIPPED: 건너뛴 단계
    """
    PLANNED = "PLANNED"           # 계획됨 (기본값)
    IN_PROGRESS = "IN_PROGRESS"   # 진행 중
    COMPLETED = "COMPLETED"       # 완료됨
    SKIPPED = "SKIPPED"           # 건너뜀


class MissionStatus(str, enum.Enum):
    """미션 상태 Enum.
    
    비즈니스 규칙:
    - PLANNED: 계획된 미션 (기본값)
    - IN_PROGRESS: 진행 중인 미션
    - COMPLETED: 완료된 미션
    - CANCELLED: 취소된 미션
    """
    PLANNED = "PLANNED"           # 계획됨 (기본값)
    IN_PROGRESS = "IN_PROGRESS"   # 진행 중
    COMPLETED = "COMPLETED"       # 완료됨
    CANCELLED = "CANCELLED"       # 취소됨
