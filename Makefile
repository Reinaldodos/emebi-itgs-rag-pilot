.PHONY: setup test

setup:
	uv sync --locked

test:
	uv run --locked pytest
