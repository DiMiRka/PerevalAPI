#!/bin/bash

alembic stamp head
alembic revision --autogenerate -m "fix_models"
alembic upgrade head

exec uvicorn src.main:app --host $HOST --port $PORT --reload
