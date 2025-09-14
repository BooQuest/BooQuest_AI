"""Celery application configuration."""

from celery import Celery
from celery.schedules import crontab
from packages.infrastructure.config.config import get_settings

# 설정 가져오기
settings = get_settings()

# Celery 앱 생성
celery_app = Celery(
    "ai_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["apps.worker.ai_tasks", "apps.worker.trend_crawling_tasks"]
)

# Celery 설정
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Seoul",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.celery_time_limit,
    task_soft_time_limit=settings.celery_soft_time_limit,
    worker_concurrency=settings.celery_worker_concurrency,
    worker_prefetch_multiplier=settings.celery_prefetch_multiplier,
)

# Task 라우팅 설정
celery_app.conf.task_routes = {
    "apps.worker.ai_tasks.*": {"queue": "ai"},
    "apps.worker.trend_crawling_tasks.*": {"queue": "trends"}
}

# 주간 스케줄 설정 (SNS 트렌드 RSS 크롤링)
celery_app.conf.beat_schedule = {
    'weekly-sns-trends': {
        'task': 'crawl_sns_trends',
        'schedule': crontab(hour=2, minute=0, day_of_week=1),  # 매주 월요일 오전 2시
    },
}

if __name__ == "__main__":
    celery_app.start()
