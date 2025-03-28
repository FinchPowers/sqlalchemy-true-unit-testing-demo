FILES := src tests

.PHONE: install
install:
	poetry install

.PHONY: format
format:
	poetry run ruff format $(FILES)
	poetry run ruff check --fix $(FILES)

.PHONY: lint
lint:
	poetry run ruff format --check $(FILES)
	poetry run ruff check $(FILES)
	poetry run mypy $(FILES)

.PHONY: test
test:
	poetry run pytest tests
