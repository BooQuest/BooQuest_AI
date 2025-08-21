FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY packages ./packages
COPY api_app ./api_app
COPY worker_app ./worker_app

ENV PYTHONPATH=/app

EXPOSE 8081

CMD ["uvicorn","api_app.main:app","--host","0.0.0.0","--port","8081"]
