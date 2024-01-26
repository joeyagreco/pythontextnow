# INSTALL DEPENDENCIES
.PHONY: deps
deps:
	@python3.10 -m pip install -r requirements.dev.txt
	@python3.10 -m pip install -r requirements.txt

# FORMAT PYTHON CODE
.PHONY: fmt
fmt:
	@black --config=pyproject.toml .
	@autoflake --config=pyproject.toml .
	@isort .

# RUN UNIT TESTS
.PHONY: test
test:
	@pytest



