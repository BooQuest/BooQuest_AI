"""LangGraph 상태 타입 정의 - 중복 제거 및 API 응답 최적화."""

from typing import TypedDict, List, Dict, Any, Optional, Union


class BaseState(TypedDict):
    """기본 상태 - 모든 노드가 공유하는 공통 필드."""
    # 공통 식별자 (필요한 경우에만 설정)
    user_id: Optional[int]
    
    # AI 생성 결과 (모든 상태에서 동일한 키 사용)
    ai_result: Optional[Dict[str, Any]]
    
    # 저장된 결과 (API 응답용)
    saved_entities: Optional[List[Dict[str, Any]]]


class SideJobState(BaseState):
    """사이드잡 생성 상태."""
    profile_data: Dict[str, Any]  # 입력 데이터
    side_job_ids: Optional[List[int]] = None  # 사이드잡 전체 재생성에만 필요한 필드
    trend_data: Optional[Dict[str, Any]] = None  # 트렌드 검색 결과


class MissionState(BaseState):
    """미션 생성 상태."""
    request_data: Dict[str, Any]  # 입력 데이터
    sidejob_id: Optional[int]     # 미션 생성에만 필요한 필드


class MissionStepState(BaseState):
    """미션 단계 생성 상태."""
    request_data: Dict[str, Any]  # 입력 데이터
    mission_id: Optional[int]      # 미션 단계 생성에만 필요한 필드

class RegenerateMissionStepState(BaseState):
    """미션 단계 재생성 상태."""
    request_data: Dict[str, Any]  # 입력 데이터
    mission_id: Optional[int]      # 미션 단계 생성에만 필요한 필드
    reasons: Optional[List[str]]  # 재생성 사유 리스트
    etc_feedback: Optional[str]  # 기타 피드백

# Union 타입으로 모든 상태를 표현
LangGraphState = Union[SideJobState, MissionState, MissionStepState]
