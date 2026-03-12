PYTHON ?= python

.PHONY: install lint format typecheck test coverage run

install:
	$(PYTHON) -m pip install -e .[dev]

lint:
	$(PYTHON) -m ruff check src tests

format:
	$(PYTHON) -m ruff format src tests

typecheck:
	$(PYTHON) -m mypy src tests

test:
	$(PYTHON) -m pytest

coverage:
	$(PYTHON) -m pytest --cov=archforge --cov-report=html --cov-report=term

run:
	$(PYTHON) -m archforge --help