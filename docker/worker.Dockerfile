FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY packages ./packages

COPY apps/worker ./apps/worker

ENV PYTHONPATH=/app LANG=C.UTF-8 LC_ALL=C.UTF-8

CMD ["celery","-A","packages.presentation.worker.celery_app.celery_app","worker","--loglevel=INFO","-I","apps.worker.ai_tasks", "-Q","ai"]
