FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY packages ./packages

COPY worker_app ./worker_app

ENV PYTHONPATH=/app

CMD ["celery","-A","packages.infrastructure.celery_app.celery_app","worker","--loglevel=INFO","-I","worker_app.tasks.ai_tasks"]
