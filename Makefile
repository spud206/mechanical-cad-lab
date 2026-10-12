.PHONY: test lint typecheck check export-example viewer jupyter

test:
	python -m pytest

lint:
	ruff check .
	ruff format --check .

typecheck:
	mypy src tests

check: lint typecheck test
	git diff --check

export-example:
	PYTHONPATH=src python scripts/export_example.py

viewer:
	python -m ocp_viewer --host 0.0.0.0 --port 3939

jupyter:
	jupyter lab --ip=0.0.0.0 --port=8888 --no-browser
