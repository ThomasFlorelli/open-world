lint:
	flake8 .
	isort --check-only .
	black --check .

format:
	isort .
	black .
