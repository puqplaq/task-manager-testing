.PHONY: run test test-cov test-allure test-load lint format lock install

install:
	poetry install

run: 
	poetry run uvicorn app.main:app --reload

test: 
	poetry run pytest tests/ -v

test-cov:
	poetry run pytest tests/ -v --cov=app --cov-report=html

test-allure:
	poetry run pytest tests/ --alluredir=allure-results
	allure generate allure-results

test-load:
	locust -f tests/load/ --host=http://127.0.0.1:8000 --headless --users 10 --spawn-rate 10 --run-time 1m

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
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov allure-results allure-report
