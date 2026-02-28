# Transformation Pipeline

This directory contains the Dagster and dbt projects for the Retail Analytics Platform.

See the root [README.md](../README.md) for full setup instructions.

## Structure

*   `dagster_project/`: Dagster definitions, resources, and sensors.
*   `dbt_project/`: dbt models (Staging, Marts) and tests.
*   `tests/`: Python unit tests.
*   `Makefile`: Local development commands for the pipeline.

## Development

Run commands inside `transformation_pipeline/` (via `make -C transformation_pipeline` or `cd transformation_pipeline`):

*   `make dev`: Start Dagster dev server.
*   `make dbt-deps`: Install dbt packages (e.g., dbt-utils).
*   `make dbt-parse`: Generate `manifest.json` for Dagster.
*   `uv run dbt build`: Run all dbt models and tests.
