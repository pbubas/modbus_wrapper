# include .env

.PHONY: clean
clean:
	find . -type d -name __pycache__ -exec rm -Rf {} +
	find . -type d -name .pytest_cache -exec rm -Rf {} +
	rm -Rf dist modbus_wrapper.egg-info build

.PHONY: build
build:
	python setup.py sdist

# setup $HOME/.pypirc for auth
.PHONY: upload
upload:
	python -m twine upload dist/*


.PHONY: upload-testpypi
upload-testpypi:
	python -m twine upload --repository testpypi dist/*
