.PHONY: setup install up down dev clean help init-db reset-db dbt-deps generate

# Load environment variables from .env file
# Use -include to allow make to start even if .env is missing (e.g. for setup)
-include .env
export

# Detect if StarRocks is local or remote
# If STARROCKS_HOST is unset, empty, localhost, or 127.0.0.1, assume LOCAL.
# Otherwise, assume REMOTE.
CHECK_HOST ?= $(if $(STARROCKS_HOST),$(STARROCKS_HOST),127.0.0.1)
ifeq ($(filter $(CHECK_HOST),127.0.0.1 localhost 0.0.0.0),)
    MODE := remote
else
    MODE := local
endif

help:
	@echo "Available commands (Mode: $(MODE)):"
	@echo "  make setup        - Install dependencies, create .env, start Docker (local only), and initialize database"
	@echo "  make install      - Install Python dependencies for all projects"
	@echo "  make up           - Start Docker containers in background (local only)"
	@echo "  make down         - Stop Docker containers (local only)"
	@echo "  make init-db      - Initialize StarRocks database and tables"
	@echo "  make reset-db     - Reset StarRocks tables and run dbt models (Prompts if remote)"
	@echo "  make generate     - Generate mock data using Ingestion Simulator"
	@echo "  make dev          - Start Dagster development server (Workspace)"
	@echo "  make test         - Run dbt tests and Python unit tests"
	@echo "  make dbt-deps     - Install dbt dependencies for all projects"
	@echo "  make clean        - Remove build artifacts and temporary files"

setup: .env install infra-check init-db dbt-deps

infra-check:
ifeq ($(MODE),local)
	@echo "📍 Local Environment Detected (Host: $(CHECK_HOST))"
	@echo "   -> Starting Docker containers..."
	$(MAKE) up
else
	@echo "☁️  Remote Environment Detected (Host: $(CHECK_HOST))"
	@echo "   -> Skipping Docker startup."
endif

.env:
	cp ingestion_simulator/.env.example .env
	@echo "Created .env from ingestion_simulator/.env.example"

install:
	$(MAKE) -C retail_analytics install
	$(MAKE) -C master_data install
	$(MAKE) -C ingestion_simulator install

up:
ifeq ($(MODE),local)
	docker-compose up -d
	@echo "Waiting for StarRocks cluster to initialize (FE + BE registration)..."
	sleep 30
else
	@echo "Skipping 'docker-compose up' (Remote Host: $(STARROCKS_HOST))"
endif

down:
ifeq ($(MODE),local)
	docker-compose down
	@echo "Services stopped."
else
	@echo "Skipping 'docker-compose down' (Remote Host: $(STARROCKS_HOST))"
endif

init-db:
	$(MAKE) -C ingestion_simulator init-db

reset-db:
ifeq ($(MODE),remote)
	@echo "⚠️  WARNING: You are about to RESET a REMOTE database at $(STARROCKS_HOST)."
	@echo "This will DROP ALL TABLES."
	@read -p "Are you sure? [y/N] " ans && [ $${ans:-N} = y ]
endif
	$(MAKE) -C ingestion_simulator reset-db
	$(MAKE) -C master_data dbt-build DBT_FLAGS="--full-refresh"
	$(MAKE) -C retail_analytics dbt-build DBT_FLAGS="--full-refresh"

dbt-deps:
	$(MAKE) -C master_data dbt-deps
	$(MAKE) -C retail_analytics dbt-deps

dev:
	# Running dagster dev from root using uv from retail_analytics (or any valid env)
	# We need a python environment to run 'dagster dev'. 
	# Strategy: Use retail_analytics's venv to run the root workspace
	# We export DAGSTER_HOME as absolute path here (removed from .env to avoid relative path error)
	# Reverting to 'dagster dev' as 'dg dev' does not support -w workspace.yaml yet
	export DAGSTER_HOME=$$(pwd)/dagster_home && uv run --project retail_analytics dagster dev -w workspace.yaml

test:
	$(MAKE) -C master_data test
	$(MAKE) -C retail_analytics test

generate:
	$(MAKE) -C ingestion_simulator generate ARGS="$(ARGS)"

clean:
	$(MAKE) -C retail_analytics clean
	$(MAKE) -C master_data clean
	$(MAKE) -C ingestion_simulator clean
	# Clean up dagster_home but preserve configuration files
	@find dagster_home -mindepth 1 -not -name "dagster.yaml" -delete 2>/dev/null || true
	@echo "Cleaned up root artifacts."
