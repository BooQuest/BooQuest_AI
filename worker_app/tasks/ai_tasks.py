import asyncio
from typing import Any, Dict
from packages.infrastructure.celery_app import celery_app
from packages.infrastructure.containers import Container

from packages.adapters.input.dto.onboarding_profile_dto import OnboardingProfileRequest
from packages.adapters.input.dto.generate_mission_request import GenerateMissionRequest
from packages.adapters.input.dto.generate_mission_step_request import GenerateMissionStepRequest
from packages.adapters.input.dto.regenerate_side_job_request import RegenerateSideJobRequest

container = Container()

@celery_app.task(name="generate_side_jobs", bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_side_jobs_task(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
    request_model = OnboardingProfileRequest(**request_data)
    usecase = container.ai_sidejob_usecase()
    result = asyncio.run(usecase.generate_side_jobs(request_model))
    return result.model_dump()

@celery_app.task(name="regenerate_side_jobs", bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def regenerate_side_jobs_task(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
    request_model = RegenerateSideJobRequest(**request_data)
    usecase = container.ai_sidejob_usecase()
    result = asyncio.run(usecase.regenerate_side_jobs(request_model))
    return result.model_dump()

@celery_app.task(name="generate_missions", bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_missions_task(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
    request_model = GenerateMissionRequest(**request_data)
    usecase = container.generate_mission_usecase()
    result = asyncio.run(usecase.generate_missions(request_model))
    return result.model_dump()

@celery_app.task(name="generate_mission_steps", bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def generate_mission_steps_task(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
    request_model = GenerateMissionStepRequest(**request_data)
    usecase = container.mission_step_generation_usecase()
    result = asyncio.run(usecase.generate_mission_steps(request_model))
    return result.model_dump()
