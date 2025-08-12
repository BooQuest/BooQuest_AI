FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    APP_PORT=8081 \
    START_CMD="uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}"

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE ${APP_PORT}

CMD ["sh","-c","$START_CMD"]
