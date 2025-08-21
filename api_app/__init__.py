"""FastAPI application package.

This package contains the FastAPI application entry point and HTTP adapters.
It depends on the shared `packages` package for business logic and DTOs, and
delegates long-running tasks to the Celery worker defined in `worker_app`.
"""
