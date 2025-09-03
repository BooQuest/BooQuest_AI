"""API 라우트."""

from fastapi import APIRouter, Depends, HTTPException, Path
from dependency_injector.wiring import inject, Provide
from typing import List
from packages.core.external.langgraph.workflow import LangGraphWorkflowService
from packages.infrastructure.di.container import Container
from packages.presentation.api.dto.request.side_job_generate_request import SideJobGenerateRequest
from packages.presentation.api.dto.request.side_job_regenerate_request import SideJobRegenerateRequest
from packages.presentation.api.dto.request.side_job_regenerate_all_request import ReGenerateAllSideJobRequest
from packages.presentation.api.dto.request.mission_generate_request import MissionGenerateRequest
from packages.presentation.api.dto.request.mission_step_generate_request import MissionStepGenerateRequest
from packages.presentation.api.dto.response.side_job_response import SideJobResponse
from packages.presentation.api.dto.response.mission_response import MissionResponse
from packages.presentation.api.dto.response.mission_step_response import MissionStepResponse
from packages.presentation.api.dto.request.regenerate_mission_steps_request import RegenerateMissionStepsRequest

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate-side-job", response_model=List[SideJobResponse])
@inject
async def side_jobs_generate(
    request: SideJobGenerateRequest,
    service: LangGraphWorkflowService = Depends(Provide[Container.langgraph_workflow])
):
    """사이드잡을 생성하고 저장합니다."""
    try:
        # AI 생성 및 저장
        saved_entities = await service.generate_side_jobs(request.model_dump())
        
        # API 응답 DTO로 변환
        return [
            SideJobResponse(
                id=entity["id"],
                title=entity["title"],
                description=entity["description"],
                is_selected=entity["is_selected"]
            )
            for entity in saved_entities
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사이드잡 생성 실패: {str(e)}")


@router.post("/generate-mission", response_model=List[MissionResponse])
@inject
async def missions_generate(
    request: MissionGenerateRequest,
    service: LangGraphWorkflowService = Depends(Provide[Container.langgraph_workflow])
):
    """미션을 생성하고 저장합니다."""
    try:
        # AI 생성 및 저장
        saved_entities = await service.generate_missions(request.model_dump())
        
        # 응답 데이터 정제 및 DTO로 변환
        response = []
        for entity in saved_entities:
            # 불필요한 필드 제거
            entity.pop("status", None)

            # MissionResponse로 변환
            response.append(
                MissionResponse(
                    id=entity["id"],
                    title=entity["title"],
                    order=entity["order_no"],
                    design_notes=entity["design_notes"],
                    guide=entity["guide"]
                )
            )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"미션 생성 실패: {str(e)}")


@router.post("/generate-mission-step", response_model=List[MissionStepResponse])
@inject
async def mission_steps_generate(
    request: MissionStepGenerateRequest,
    service: LangGraphWorkflowService = Depends(Provide[Container.langgraph_workflow])
):
    """미션 단계를 생성하고 저장합니다."""
    try:
        print("Request Data:", request.model_dump())
        # AI 생성 및 저장
        saved_entities = await service.generate_mission_steps(request.model_dump())
        
        # API 응답 DTO로 변환
        return [
            MissionStepResponse(
                id=entity["id"],
                seq=entity["seq"],
                title=entity["title"],
                detail=entity["detail"]
            )
            for entity in saved_entities
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"미션 단계 생성 실패: {str(e)}")
    
@router.post("/regenerate-side-job-all", response_model=List[SideJobResponse])
@inject
async def side_jobs_generate_all(
    request: ReGenerateAllSideJobRequest,
    service: LangGraphWorkflowService = Depends(Provide[Container.langgraph_workflow])
):
    """사이드잡을 생성하고 저장합니다."""
    try:
        # AI 생성 및 저장
        saved_entities = await service.regenerate_all_side_jobs(request.model_dump())
        
        # API 응답 DTO로 변환
        return [
            SideJobResponse(
                id=entity["id"],
                title=entity["title"],
                description=entity["description"],
                is_selected=entity["is_selected"]
            )
            for entity in saved_entities
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사이드잡 재생성 실패: {str(e)}")


@router.post("/regenerate-side-job/{sideJobId}", response_model=SideJobResponse)
@inject
async def side_jobs_regenerate(
    request: SideJobRegenerateRequest,
    sideJobId: int = Path(..., description="재생성할 사이드잡 ID"),
    service: LangGraphWorkflowService = Depends(Provide[Container.langgraph_workflow])
):
    """사이드잡을 재생성하고 저장합니다."""
    try:
        data = request.model_dump()
        data["side_job_id"] = sideJobId
        
        # AI 재생성 및 저장
        entity = await service.regenerate_side_job(data)
        
        # API 응답 DTO로 변환
        return SideJobResponse(
            id=entity["id"],
            title=entity["title"],
            description=entity["description"],
            is_selected=entity["is_selected"]
        )
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사이드잡 재생성 실패: {str(e)}")

@router.post("/regenerate-mission-step", response_model=List[MissionStepResponse])
@inject
async def side_jobs_generate_all(
    request: RegenerateMissionStepsRequest,
    service: LangGraphWorkflowService = Depends(Provide[Container.langgraph_workflow])
):
    """사이드잡을 생성하고 저장합니다."""
    try:
        # AI 생성 및 저장
        saved_entities = await service.regenerate_mission_steps(request.model_dump())
        
        # API 응답 DTO로 변환
        return [
            MissionStepResponse(
                id=entity["id"],
                seq=entity["seq"],
                title=entity["title"],
                detail=entity["detail"]
            )
            for entity in saved_entities
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"부퀘스트 재생성 실패: {str(e)}")

# 상태 확인용 라우터
status_router = APIRouter(prefix="/status", tags=["Status"])

@status_router.get("/health")
async def health_check():
    """헬스 체크."""
    return {"status": "healthy"}

router.include_router(status_router)
