.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: build
build:
	rm -rf dist/
	python3 -m build

.PHONY: publish-test
publish-test: build
	python3 -m twine upload --repository testpypi dist/*

.PHONY: venv-test
venv-test:
	python3 -m venv .venv
	. .venv/bin/activate
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dancesport-parser