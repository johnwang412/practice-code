#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! pg_isready -h postgres -p 5432 -U postgres; do
    echo "PostgreSQL is not ready yet. Waiting..."
    sleep 2
done

echo "PostgreSQL is ready!"

# Run Alembic migrations
echo "Running database migrations..."
alembic -c alembic/alembic.ini upgrade head

# Start the FastAPI application
echo "Starting FastAPI application..."
exec uvicorn api.url_api:app --host 0.0.0.0 --port 8000 --workers 8
