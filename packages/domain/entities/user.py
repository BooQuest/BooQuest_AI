"""User SQLAlchemy ORM 모델."""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Text
from datetime import datetime
from .base import Base


class User(Base):
    """사용자 ORM 모델."""
    __tablename__ = "users"
    
    # Primary Key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # 사용자 정보
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    social_nickname: Mapped[str] = mapped_column(String(100), nullable=True)
    profile_image_url: Mapped[str] = mapped_column(Text, nullable=True)
    
    # 소셜 로그인 정보
    provider: Mapped[str] = mapped_column(String(50), nullable=True)
    provider_user_id: Mapped[str] = mapped_column(String(255), nullable=True)
    
    # 시간 정보
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', nickname='{self.nickname}')>"
