"""API 라우터."""

from typing import List
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from packages.infrastructure.di.container import Container
from packages.presentation.api.dto.request.generate_side_job_request import GenerateSideJobRequest
from packages.presentation.api.dto.request.mission_generate_request import MissionGenerateRequest
from packages.presentation.api.dto.request.mission_step_generate_request import MissionStepGenerateRequest
from packages.presentation.api.dto.request.regenerate_side_job_request import RegenerateSideJobRequest
from packages.presentation.api.dto.response.mission_response import MissionResponse
from packages.presentation.api.dto.response.mission_step_response import MissionStepResponse
from packages.presentation.api.dto.response.side_job_response import SideJobResponse

# 라우터
router = APIRouter(prefix="/ai", tags=["AI"])

# 동기 처리로 AI 생성 및 저장 후 실제 response 반환
@router.post("/generate-side-job", response_model=List[SideJobResponse])
@inject
async def sidejobs_generate(
    request: GenerateSideJobRequest,
    service = Depends(Provide[Container.langgraph_workflow])
):
    """사이드잡을 생성하고 저장합니다."""
    result = await service.generate_side_jobs(request.model_dump())
    
    # AI 생성된 실제 데이터를 Response DTO로 변환하여 반환
    return [
        SideJobResponse(
            id=job["id"],
            title=job["title"],
            description=job["description"]
        )
        for job in result
    ]


@router.post("/generate-mission", response_model=List[MissionResponse])
@inject
async def missions_generate(
    request: MissionGenerateRequest,
    service = Depends(Provide[Container.langgraph_workflow])
):
    """미션을 생성하고 저장합니다."""
    result = await service.generate_missions(request.model_dump())
    
    # AI 생성된 실제 데이터를 Response DTO로 변환하여 반환
    return [
        MissionResponse(
            id=mission["id"],
            title=mission["title"],
            order=mission["orderNo"],
            design_notes=mission["notes"]
        )
        for mission in result
    ]


@router.post("/generate-mission-step", response_model=List[MissionStepResponse])
@inject
async def mission_steps_generate(
    request: MissionStepGenerateRequest,
    service = Depends(Provide[Container.langgraph_workflow])
):
    result = await service.generate_mission_steps(request.model_dump())
    
    # AI 생성된 실제 데이터를 Response DTO로 변환하여 반환
    return [
        MissionStepResponse(
            id=step["id"],
            title=step["title"],
            seq=step["seq"],
            status=step["status"],
            detail=step["detail"]
        )
        for step in result
    ]


@router.post("/regenerate-side-job", response_model=List[SideJobResponse])
@inject
async def sidejobs_regenerate(
    request: RegenerateSideJobRequest,
    service = Depends(Provide[Container.langgraph_workflow])
):
    """피드백을 바탕으로 사이드잡을 재생성하고 저장합니다."""
    result = await service.regenerate_side_jobs(request.dict())
    
    # AI 생성된 실제 데이터를 Response DTO로 변환하여 반환
    return [
        SideJobResponse(
            id=job["id"],
            title=job["title"],
            description=job["description"]
        )
        for job in result
    ]


# 상태 확인용 라우터
status_router = APIRouter(prefix="/status", tags=["Status"])

@status_router.get("/health")
async def health_check():
    """헬스 체크."""
    return {"status": "healthy"}

router.include_router(status_router)
