.PHONY: setup install up down dev clean help

# Load environment variables from .env file
# Use -include to allow make to start even if .env is missing (e.g. for setup)
-include .env
export

help:
	@echo "Available commands:"
	@echo "  make setup        - Install dependencies, create .env, start Docker, and initialize database"
	@echo "  make install      - Install Python dependencies for all projects"
	@echo "  make up           - Start Docker containers in background"
	@echo "  make down         - Stop Docker containers"
	@echo "  make init-db      - Initialize StarRocks database and tables"
	@echo "  make reset-db     - Reset StarRocks tables and run dbt models"
	@echo "  make generate     - Generate mock data using Ingestion Simulator"
	@echo "  make dev          - Start Dagster development server"
	@echo "  make dbt-deps     - Install dbt dependencies"
	@echo "  make clean        - Remove build artifacts and temporary files"

setup: .env install up init-db dbt-deps

.env:
	cp ingestion_simulator/.env.example .env
	@echo "Created .env from ingestion_simulator/.env.example"

install:
	$(MAKE) -C transformation_pipeline install
	$(MAKE) -C ingestion_simulator install

up:
	docker-compose up -d
	@echo "Waiting for services to be ready..."
	sleep 10

down:
	docker-compose down
	@echo "Services stopped."

init-db:
	$(MAKE) -C ingestion_simulator init-db

reset-db:
	$(MAKE) -C ingestion_simulator reset-db
	$(MAKE) -C transformation_pipeline dbt-build

dbt-deps:
	$(MAKE) -C transformation_pipeline dbt-deps

dev:
	$(MAKE) -C transformation_pipeline dev

generate:
	$(MAKE) -C ingestion_simulator generate ARGS="$(ARGS)"

clean:
	$(MAKE) -C transformation_pipeline clean
	$(MAKE) -C ingestion_simulator clean
