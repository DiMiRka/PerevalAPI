FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
ENV DOCKER_MODE=1

COPY requirements.txt .
COPY .env.docker .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]