FROM python:3.11-slim

RUN mkdir -p /app
WORKDIR /app


ENV PYTHONPATH=/app/src
ENV DOCKER_MODE=1

COPY --chmod=777 requirements.txt .
COPY --chmod=777 .env.docker .
COPY --chmod=777 docker-entrypoint.sh .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chmod=777 . .

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]