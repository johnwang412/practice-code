FROM python:3.11-slim

# Install PostgreSQL client for pg_isready
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

# Make startup script executable
RUN chmod +x /app/startup.sh

EXPOSE 8000

WORKDIR /app/

ENV PYTHONPATH=.

CMD ["./startup.sh"]