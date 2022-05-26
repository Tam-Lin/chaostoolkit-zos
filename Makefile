.PHONY: install
install:
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt

.PHONY: install-dev
install-dev: install
	pip install -r requirements-dev.txt
	python setup.py develop

.PHONY: lint
lint:
	flake8 chaoszos/ tests/
	isort --check-only --profile black chaoszos/ tests/
	black --check --diff chaoszos/ tests/

.PHONY: format
format:
	isort --profile black chaoszos/ tests/
	black chaoszos/ tests/

.PHONY: tests
tests:
	pytest
