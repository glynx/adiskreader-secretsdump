clean:
	rm -f -r build/
	rm -f -r dist/
	rm -f -r *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +

publish: clean build
	python3 -m twine upload dist/*

rebuild: clean
	pip install .

build:
	pip wheel . -w dist --no-deps

# uv workflows (the adiskreader fork checkout is expected at ../adiskreader)
dev:
	uv sync --extra dev

run:
	uv run adiskreader-secretsdump

install:
	uv tool install --force .

install-editable:
	uv tool install --force --editable .
