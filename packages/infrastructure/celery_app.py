
from celery import Celery

from packages.infrastructure.config import get_settings  # type: ignore


def create_celery_app() -> Celery:
    """설정에 기반하여 Celery 인스턴스를 생성합니다."""
    settings = get_settings()
    celery = Celery(
        "app_tasks",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
        include=[  # 명시적 포함
            "worker_app.tasks.ai_tasks",
        ],
    )

    # 직렬화/역직렬화 포맷 설정
    celery.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        # 운영 기본
        worker_prefetch_multiplier=settings.celery_prefetch_multiplier,
        task_acks_late=True,                 # 워커 장애 시 재배포
        task_reject_on_worker_lost=True,
        task_time_limit=settings.celery_time_limit,
        task_soft_time_limit=settings.celery_soft_time_limit,
        task_routes={
            # 태스크별 큐/route 지정 가능
            "generate_side_jobs": {"queue": "ai"},
            "generate_missions": {"queue": "ai"},
            "generate_mission_steps": {"queue": "ai"},
            "regenerate_side_jobs": {"queue": "ai"},
        },
    )
    return celery


# 기본 Celery 인스턴스. 여러 모듈에서 재사용됩니다.
celery_app = create_celery_app()