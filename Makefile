.PHONY: up down init test check
up:
	python scripts/dev.py up
down:
	python scripts/dev.py down
init:
	python scripts/dev.py init
test:
	uv run python scripts/backend_checks.py
check:
	python scripts/checks.py
