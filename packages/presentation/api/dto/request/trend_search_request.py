"""트렌드 검색 요청 DTO."""

from pydantic import BaseModel, Field
from typing import Optional, List


class TrendSearchRequest(BaseModel):
    """트렌드 검색 요청."""
    
    query: str = Field(..., description="검색 쿼리", min_length=1, max_length=500)
    limit: int = Field(default=10, description="검색 결과 개수", ge=1, le=100)
    platform: Optional[str] = Field(default=None, description="플랫폼 필터 (instagram, tiktok, legal)")
    trend_type: Optional[str] = Field(default=None, description="트렌드 타입 필터 (hashtag, content, challenge, legal)")
    similarity_threshold: Optional[float] = Field(default=0.7, description="유사도 임계값", ge=0.0, le=1.0)
