PROJECT_NAME = crypto_VDF

PYTHON = python

M = $(shell printf "\033[34;1m▶\033[0m")

.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Available targets:"
	@echo "$(M) help          - Display this help message"
	@echo "$(M) deps          - Install dependencies"
	@echo "$(M) deps-tests    - Install dependencies for tests"
	@echo "$(M) tests         - Run tests"
	@echo "$(M) coverage      - Run coverage tests"
	@echo "$(M) lint          - Run flake8 for linting"

.PHONY: deps
deps:
	@$(info $(M) installing dependencies...)
	pip install -r requirements.txt


.PHONY: deps-tests
deps-tests:
	@$(info $(M) installing dependencies for tests...)
	pip install -r requirements-tests.txt


.PHONY: tests
tests:
	@$(info $(M) testing package...)
	pip install -e . > /dev/null && pip install pytest > /dev/null
	python -m pytest tests

.PHONY: coverage
coverage:
	@$(info $(M) coverage testing package...)
	pip install -e . > /dev/null && pip install pytest pytest-cov > /dev/null
	python -m pytest tests --cov=$(PROJECT_NAME) --cov-fail-under=0

.PHONY: lint
lint:
	@$(info $(M) coverage testing package...)
	pip install -e . > /dev/null && pip install flake8 > /dev/null
	flake8 src/$(PROJECT_NAME)