"""Celery Worker 엔트리 포인트."""

from packages.presentation.worker.celery_app import celery_app

if __name__ == "__main__":
    celery_app.start()
