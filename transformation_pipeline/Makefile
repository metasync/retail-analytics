.PHONY: install dev test clean dbt-build dbt-deps

# Load environment variables from root .env
include ../.env
export

# Ensure DBT_PROJECT_DIR is relative to this makefile
DBT_PROJECT_DIR=dbt_project
DBT_PROFILES_DIR=dbt_project

install:
	uv sync

dev:
	uv run dg dev

test:
	uv run dbt test --project-dir $(DBT_PROJECT_DIR) --profiles-dir $(DBT_PROFILES_DIR) --target $(DBT_TARGET)
	uv run pytest tests

dbt-deps:
	uv run dbt deps --project-dir $(DBT_PROJECT_DIR) --profiles-dir $(DBT_PROFILES_DIR)
	uv run dbt parse --project-dir $(DBT_PROJECT_DIR) --profiles-dir $(DBT_PROFILES_DIR)

dbt-build:
	uv run dbt build --project-dir $(DBT_PROJECT_DIR) --profiles-dir $(DBT_PROFILES_DIR) --target $(DBT_TARGET) $(if $(DBT_SELECT),--select $(DBT_SELECT)) $(DBT_FLAGS)

clean:
	@rm -rf .venv
	@rm -rf dbt_project/target
	@rm -rf dbt_project/logs
	@rm -rf dbt_project/dbt_packages
	@rm -rf .tmp_*
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "Cleaned up transformation_pipeline."
