.PHONY: dev build

.venv:
	python -m venv .venv

dev: .venv
	.venv/bin/pip install -r app-shortener/requirements.txt

local-up:
	docker-compose up -d
	docker-compose logs -f

local-down:
	docker-compose down

build:
	docker-compose build