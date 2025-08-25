"""Celery application configuration."""

from celery import Celery
from packages.infrastructure.config.config import get_settings

# 설정 가져오기
settings = get_settings()

# Celery 앱 생성
celery_app = Celery(
    "ai_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["apps.worker.ai_tasks"]
)

# Celery 설정
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30분
    task_soft_time_limit=25 * 60,  # 25분
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Task 라우팅 설정
celery_app.conf.task_routes = {
    "apps.worker.ai_tasks.*": {"queue": "ai"}
}

if __name__ == "__main__":
    celery_app.start()
