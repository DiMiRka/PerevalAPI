#!/bin/bash


alembic upgrade head

exec uvicorn src.main:app --host $HOST --port $PORT --reload
