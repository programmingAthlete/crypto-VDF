PROJECT_NAME = crypto-VDF

PYTHON = python

.PHONY: deps
deps: $(info $(M) installing dependencies...)
	pip install -r requirements.txt


.PHONY: deps-tests
deps-tests: $(info $(M) installing dependencies for tests...)
	pip install -r requirements-tests.txt


.PHONY: tests
tests: $(info $(M) testing package...)
	pip install -e . > /dev/null && pip install pytest > /dev/null
	python -m pytest tests

.PHONY: coverage
coverage: $(info $(M) coverage testing package...)  ## test coverage package
	pip install -e . > /dev/null && pip install pytest pytest-cov > /dev/null
	python -m pytest tests --cov=$(PROJECT_NAME) --cov-fail-under=0
