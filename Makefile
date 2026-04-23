PROJECT?=heimdall

lint:
	@uv --directory $(PROJECT) run ruff format
	@uv --directory $(PROJECT) run ruff check --fix