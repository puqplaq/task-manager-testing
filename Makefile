.PHONY: run test test-cov lint format lock install

install:
	poetry install

run: 
	poetry run uvicorn app.main:app --reload

test: 
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ -v --cov=app --cov-report=html

lint:
	poetry run ruff check app/ tests/
	poetry run mypy app/

fix:
	poetry run ruff check --fix app/ tests/

format:
	poetry run ruff format app/ tests/

lock:
	poetry lock

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov