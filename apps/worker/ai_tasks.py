"""AI generation Celery tasks using LangGraph Workflow."""

from celery import shared_task
from typing import Dict, Any
from packages.infrastructure.constants.task_names import TaskName
from packages.infrastructure.di.container import container
from packages.infrastructure.logging import get_logger

logger = get_logger(__name__)


@shared_task(
    name=TaskName.GENERATE_SIDE_JOBS,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def generate_side_jobs_task(
    self,
    user_id: int,
    job: str,
    hobbies: list,
    expression_style: str,
    strength_type: str
) -> Dict[str, Any]:
    """사이드잡 생성을 위한 Celery task (Workflow 사용)."""
    try:
        logger.info(f"사이드잡 생성 시작: user_id={user_id}")
        # 컨테이너에서 Workflow 서비스 가져오기
        workflow = container.langgraph_workflow()
        
        # Workflow를 사용하여 사이드잡 생성 및 저장
        # 동기적으로 실행 (Celery task 내에서)
        import asyncio
        
        # 이벤트 루프가 없으면 새로 생성
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Workflow 실행
        result = loop.run_until_complete(
            workflow.generate_side_jobs({
                "user_id": user_id,
                "job": job,
                "hobbies": hobbies,
                "expression_style": expression_style,
                "strength_type": strength_type
            })
        )
        
        logger.info(f"사이드잡 생성 완료: user_id={user_id}")
        return {
            "status": "success",
            "task_id": self.request.id,
            "result": result
        }
        
    except Exception as e:
        logger.error(f"사이드잡 생성 실패: user_id={user_id}, error={e}")
        # 재시도 로직
        raise self.retry(countdown=60, exc=e)


@shared_task(
    name=TaskName.GENERATE_MISSIONS,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def generate_missions_task(
    self,
    user_id: int,
    side_job_id: int,
    side_job_title: str,
    side_job_design_notes: str
) -> Dict[str, Any]:
    """미션 생성을 위한 Celery task (Workflow 사용)."""
    try:
        # 컨테이너에서 Workflow 서비스 가져오기
        workflow = container.langgraph_workflow()
        
        # Workflow를 사용하여 미션 생성 및 저장
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Workflow 실행
        result = loop.run_until_complete(
            workflow.generate_missions({
                "user_id": user_id,
                "sidejob_id": side_job_id,
                "side_job_title": side_job_title,
                "side_job_design_notes": side_job_design_notes
            })
        )
        
        return {
            "status": "success",
            "task_id": self.request.id,
            "result": result
        }
        
    except Exception as e:
        raise self.retry(countdown=60, exc=e)


@shared_task(
    name=TaskName.GENERATE_MISSION_STEPS,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def generate_mission_steps_task(
    self,
    user_id: int,
    mission_id: int,
    mission_title: str,
    mission_design_notes: str
) -> Dict[str, Any]:
    """미션 단계 생성을 위한 Celery task (Workflow 사용)."""
    try:
        # 컨테이너에서 Workflow 서비스 가져오기
        workflow = container.langgraph_workflow()
        
        # Workflow를 사용하여 미션 단계 생성 및 저장
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Workflow 실행
        result = loop.run_until_complete(
            workflow.generate_mission_steps({
                "user_id": user_id,
                "mission_id": mission_id,
                "mission_title": mission_title,
                "mission_design_notes": mission_design_notes
            })
        )
        
        return {
            "status": "success",
            "task_id": self.request.id,
            "result": result
        }
        
    except Exception as e:
        raise self.retry(countdown=60, exc=e)


@shared_task(
    name=TaskName.REGENERATE_SIDE_JOBS,
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3
)
def regenerate_side_jobs_task(
    self,
    user_id: int,
    generate_side_job_request: dict,
    feedback_data: dict
) -> Dict[str, Any]:
    """사이드잡 재생성을 위한 Celery task (Workflow 사용)."""
    try:
        # 컨테이너에서 Workflow 서비스 가져오기
        workflow = container.langgraph_workflow()
        
        # Workflow를 사용하여 사이드잡 재생성 및 저장
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Workflow 실행
        result = loop.run_until_complete(
            workflow.regenerate_side_jobs({
                "user_id": user_id,
                "generate_side_job_request": generate_side_job_request,
                "feedback_data": feedback_data
            })
        )
        
        return {
            "status": "success",
            "task_id": self.request.id,
            "result": result
        }
        
    except Exception as e:
        raise self.retry(countdown=60, exc=e)
