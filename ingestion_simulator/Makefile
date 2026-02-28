.PHONY: install init-db reset-db generate clean help generate-help

# Load environment variables from root .env
include ../.env
export

install:
	uv sync

init-db:
	uv run ingest starrocks init

reset-db:
	uv run ingest starrocks reset

generate:
	uv run ingest data generate $(ARGS)

generate-help:
	uv run ingest data generate --help

clean:
	rm -rf .venv
	rm -f requirements.txt
	find . -type d -name "__pycache__" -exec rm -rf {} +

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make init-db      - Initialize StarRocks DB"
	@echo "  make reset-db     - Reset StarRocks DB"
	@echo "  make generate     - Generate data (use ARGS='...' for options)"
	@echo "  make generate-help- Show options for generate"
