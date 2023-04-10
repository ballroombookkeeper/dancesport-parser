.PHONY: help
help:
	@LC_ALL=C $(MAKE) -pRrq -f $(firstword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/(^|\n)# Files(\n|$$)/,/(^|\n)# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

venv-dev: requirements.txt
	python3 -m venv .venv-dev
	. .venv-dev/bin/activate; pip3 install -r requirements-dev.txt; pip3 install -r requirements.txt

.PHONY: build
build:
	rm -rf dist/
	python3 -m build

.PHONY: publish-test
publish-test: build
	python3 -m twine upload --repository testpypi dist/*

.PHONY: publish
publish: build
	python3 -m twine upload dist/*

.PHONY: venv-test
venv-test:
	python3 -m venv .venv-test
	. .venv-test/bin/activate
	python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps dancesport-parser

.PHONY: test
test: venv-dev
	. .venv-dev/bin/activate; pytest