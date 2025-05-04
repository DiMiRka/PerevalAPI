#!/bin/bash

until pg_isready -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

alembic upgrade head

exec uvicorn src.main:app --host $HOST --port $PORT --reload
