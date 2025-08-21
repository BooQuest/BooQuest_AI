"""FastAPI router for AI-related endpoints.

This router defines HTTP endpoints that accept Pydantic request models,
enqueue Celery tasks for long-running AI generation work, and return
the result once available.  Celery tasks are defined in the ``worker_app``
package and use the shared business logic from the ``packages`` package.
"""

from multiprocessing.pool import AsyncResult
from fastapi import APIRouter
import asyncio

from packages.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from packages.adapters.input.dto.generate_mission_response import GenerateMissionReponse
from packages.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from packages.adapters.input.dto.generate_mission_step_response import GenerateMissionStepResponse
from packages.adapters.input.dto.onboarding_profile_dto import OnboardingProfileRequest
from packages.adapters.input.dto.regenerate_side_job_request import RegenerateSideJobRequest
from packages.adapters.input.dto.side_job_response import SideJobResponse

# Import Celery tasks from the worker package.  These tasks will be executed
# by the Celery worker defined in worker_app and use the shared business
# logic in packages.
from worker_app.tasks.ai_tasks import (
    generate_side_jobs_task,
    regenerate_side_jobs_task,
    generate_missions_task,
    generate_mission_steps_task,
)


ai_router = APIRouter(prefix="/ai", tags=["AI"])


@ai_router.post("/generate-side-job", response_model=SideJobResponse)
async def generate_side_job(request: OnboardingProfileRequest) -> SideJobResponse:
    """Generate side jobs based on the onboarding profile via Celery."""
    # Celery 작업에 요청을 위임하고 결과를 기다립니다.
    task = generate_side_jobs_task.delay(request.model_dump())
    result_dict = await asyncio.get_event_loop().run_in_executor(None, task.get)
    return SideJobResponse(**result_dict)


@ai_router.post("/generate-mission", response_model=GenerateMissionReponse)
async def generate_missions(request: GenerateMissionRequest) -> GenerateMissionReponse:
    """Generate missions via Celery."""
    task = generate_missions_task.delay(request.model_dump())
    result_dict = await asyncio.get_event_loop().run_in_executor(None, task.get)
    return GenerateMissionReponse(**result_dict)


@ai_router.post("/generate-mission-step", response_model=GenerateMissionStepResponse)
async def generate_mission_steps(request: GenerateMissionStepRequest) -> GenerateMissionStepResponse:
    """Generate mission steps via Celery."""
    task = generate_mission_steps_task.delay(request.model_dump())
    result_dict = await asyncio.get_event_loop().run_in_executor(None, task.get)
    return GenerateMissionStepResponse(**result_dict)


@ai_router.post("/regenerate-side-job", response_model=SideJobResponse)
async def regenerate_side_job(request: RegenerateSideJobRequest) -> SideJobResponse:
    """Regenerate side jobs based on feedback via Celery."""
    task = regenerate_side_jobs_task.delay(request.model_dump())
    result_dict = await asyncio.get_event_loop().run_in_executor(None, task.get)
    return SideJobResponse(**result_dict)

# 태스크 상태/결과 조회
status_router = APIRouter(prefix="/tasks", tags=["Tasks"])

@status_router.get("/{task_id}")
def task_status(task_id: str):
    r = AsyncResult(task_id)
    return {"task_id": task_id, "state": r.state, "ready": r.ready(), "successful": r.successful()}

@status_router.get("/{task_id}/result")
def task_result(task_id: str):
    r = AsyncResult(task_id)
    if not r.ready():
        return {"task_id": task_id, "state": r.state, "ready": False}
    if r.failed():
        return {"task_id": task_id, "state": r.state, "ready": True, "error": str(r.result)}
    return {"task_id": task_id, "state": r.state, "ready": True, "result": r.result}