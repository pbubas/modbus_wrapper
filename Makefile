include .env

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -Rf {} +
	find . -type d -name .pytest_cache -exec rm -Rf {} +
	rm -Rf dist modbus_wrapper.egg-info build

.PHONY: build
build:
	python setup.py sdist

.PHONY: upload
export $(TWINE_USERNAME)
export $(TWINE_PASSWORD)
upload:
	python -m twine upload dist/*


.PHONY: upload-testpypi
export TWINE_USERNAME=$(TESTPYPI_TWINE_USERNAME)
export TWINE_PASSWORD=$(TESTPYPI_TWINE_PASSWORD)
upload-testpypi:
	python -m twine upload --repository testpypi dist/*
