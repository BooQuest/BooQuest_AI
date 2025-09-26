"""AI 응답 모델 DTO - AI 질문에 대한 응답."""

from typing import List
from pydantic import BaseModel, Field


class SideJobAIResponse(BaseModel):
    """AI가 생성하는 사이드잡 응답 모델."""
    title: str = Field(..., description="[분위기] + [주제] + [형식] + [플랫폼] 형태의 제목")
    description: str = Field(..., description="상세 설명 및 구체적인 실행 방안")


class SideJobsAIResponse(BaseModel):
    """AI가 생성하는 사이드잡 목록 응답 모델."""
    side_jobs: List[SideJobAIResponse] = Field(..., description="사이드잡 목록")
    prompt_meta: str = Field(default="", description="프롬프트 메타데이터")


class GuideAiResponse(BaseModel):
    """AI가 생성하는 미션 가이드"""
    guide_title:str = Field(..., description="가이드 제목")
    description:str = Field(..., description="가이드 상세 설명")
    
class MissionAIResponse(BaseModel):
    """AI가 생성하는 미션 응답 모델."""
    title: str = Field(..., description="미션 제목")
    orderNo: int = Field(..., description="미션 순서 번호")
    notes: str = Field(..., description="미션 노트")
    guide: List[GuideAiResponse] = Field(..., description="미션 가이드")


class MissionsAIResponse(BaseModel):
    """AI가 생성하는 미션 목록 응답 모델."""
    missions: List[MissionAIResponse] = Field(..., description="미션 목록")


class MissionStepAIResponse(BaseModel):
    """AI가 생성하는 미션 단계 응답 모델."""
    title: str = Field(..., description="단계 제목")
    seq: int = Field(..., description="단계 순서")
    detail: str = Field(..., description="단계 상세 내용")


class MissionStepsAIResponse(BaseModel):
    """AI가 생성하는 미션 단계 목록 응답 모델."""
    mission_steps: List[MissionStepAIResponse] = Field(..., description="미션 단계 목록")
