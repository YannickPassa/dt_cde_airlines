# Delete target on error.
# https://www.gnu.org/software/make/manual/html_node/Errors.html#Errors
# > This is almost always what you want make to do, but it is not historical
# > practice; so for compatibility, you must explicitly request it
.DELETE_ON_ERROR:

REQUIREMENTS_PATH ?= requirements/dev.txt

VIRTUAL_ENV ?= .venv
export PATH := $(VIRTUAL_ENV)/bin:$(PATH)


# Python
# =============================================================================
.PHONY: venv compile-deps

PYTHON ?= python3.13

$(VIRTUAL_ENV): $(REQUIREMENTS_PATH)
	uv venv --python $(PYTHON)
	uv pip sync --require-hashes $^
	touch $@
venv: $(VIRTUAL_ENV)

PIP_COMPILE_FLAGS := --generate-hashes $(PIP_COMPILE_OPTIONS)
compile-deps: $(VIRTUAL_ENV)
	uv pip compile $(PIP_COMPILE_FLAGS) -o requirements/base.txt requirements/base.in
	uv pip compile $(PIP_COMPILE_FLAGS) -o requirements/dev.txt requirements/dev.in