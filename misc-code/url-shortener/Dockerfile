FROM python:3.11-slim

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8000

WORKDIR /app/

ENV PYTHONPATH=api

CMD ["uvicorn", "api.url_api:app", "--host", "0.0.0.0", "--port", "8000"]