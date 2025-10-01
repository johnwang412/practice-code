# Overview

URL shortener

# Usage

- Postgres running in Docker
    - `make local-up`
- App server running on local machine
    - `uvicorn api.url_api:app --host 0.0.0.0 --port 8000 --workers 8`
- Using locust testing with script. Only making PUT requests to insert new
records.
    - `locust -f integration-tests/locust-load-test.py`