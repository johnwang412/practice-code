docker:
	docker build -t kv-store .

local-env: .venv
	.venv/bin/pip install -r requirements-dev.txt

.venv:
	python3 -m venv .venv
