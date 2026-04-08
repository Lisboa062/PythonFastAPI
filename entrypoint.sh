#!/bin/sh

echo "Aplicando migration..."
alembic upgrade head

echo "Iniciando API..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
