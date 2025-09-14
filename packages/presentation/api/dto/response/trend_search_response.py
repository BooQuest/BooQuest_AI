"""트렌드 검색 응답 DTO."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class TrendSearchResult(BaseModel):
    """트렌드 검색 결과."""
    
    id: int = Field(..., description="트렌드 ID")
    platform: str = Field(..., description="플랫폼")
    trend_type: str = Field(..., description="트렌드 타입")
    title: str = Field(..., description="제목")
    content: str = Field(..., description="내용")
    url: Optional[str] = Field(None, description="URL")
    tags: Optional[List[str]] = Field(None, description="태그")
    engagement_metrics: Optional[Dict[str, Any]] = Field(None, description="참여 지표")
    legal_implications: Optional[str] = Field(None, description="법적 동향")
    created_at: datetime = Field(..., description="생성일시")
    similarity_score: Optional[float] = Field(None, description="유사도 점수")


class TrendSearchResponse(BaseModel):
    """트렌드 검색 응답."""
    
    query: str = Field(..., description="검색 쿼리")
    total_count: int = Field(..., description="총 검색 결과 수")
    results: List[TrendSearchResult] = Field(..., description="검색 결과")
    search_time_ms: int = Field(..., description="검색 소요 시간 (밀리초)")
