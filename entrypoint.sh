#!/bin/sh

echo "Aplicando migration..."
alembic upgrade head

echo "Iniciando API..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
