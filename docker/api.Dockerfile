FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY packages ./packages
COPY apps/api ./apps/api

ENV PYTHONPATH=/app LANG=C.UTF-8 LC_ALL=C.UTF-8

EXPOSE 8081

CMD ["uvicorn","apps.api.main:app","--host","0.0.0.0","--port","8081"]
