# Retail Analytics Platform

A realistic data platform built with **Dagster**, **dbt**, and **StarRocks**.

## Architecture

This project follows a decoupled monorepo architecture:

1.  **Ingestion Simulator** (`ingestion_simulator/`):
    *   A standalone Python CLI tool (`ingest`).
    *   Generates mock retail data (Customers, Products, Orders).
    *   Ingests data directly into StarRocks using **Stream Load**.
    *   Manages database lifecycle (Init, Reset).

2.  **Transformation Pipeline** (`transformation_pipeline/`):
    *   A Dagster project managing the data lifecycle.
    *   **dbt** models transform raw data (`raw_orders` etc.) into dimensional models (`dim_customers`, `fact_sales`).
    *   Dagster assets observe StarRocks tables and trigger dbt runs.

## Prerequisites

*   Python 3.12+
*   Docker & Docker Compose
*   `uv` (Package Manager) - [Install uv](https://github.com/astral-sh/uv)

## Quick Start

1.  **Setup Environment**:
    Install dependencies, start StarRocks (Docker), and initialize the database.
    ```bash
    make setup
    ```

2.  **Start Dagster**:
    Launch the Dagster UI (available at http://localhost:3000).
    ```bash
    make dev
    ```

3.  **Generate Data**:
    In a new terminal, generate mock data and load it into StarRocks.
    ```bash
    make generate
    ```
    You will see logs indicating successful Stream Load.

4.  **Observe & Transform**:
    *   Go to Dagster UI (Overview > Jobs).
    *   The `check_sources_job` runs every minute to detect new data.
    *   Once data is detected, the `default_automation_condition_sensor` will automatically trigger the dbt models (`stg_*` -> `dim_*`, `fact_*`).
    *   You can also manually materialize assets if you prefer.

## Project Structure

*   `ingestion_simulator/`: Data generation tool.
    *   `src/`: Python source code.
    *   `Makefile`: Simulator-specific commands.
*   `transformation_pipeline/`: Data pipeline.
    *   `dagster_project/`: Dagster assets and definitions.
    *   `dbt_project/`: dbt models and tests.
*   `docker-compose.yml`: Infrastructure (StarRocks).
*   `Makefile`: Root orchestrator.

## Commands

*   `make setup`: Full setup (install, up, init-db).
*   `make install`: Install Python dependencies (using `uv`).
*   `make up`: Start StarRocks containers.
*   `make down`: Stop containers.
*   `make init-db`: Initialize StarRocks database/tables.
*   `make reset-db`: Reset database (DROP/CREATE) and re-run dbt models.
*   `make generate`: Generate and load mock data.
*   `make dev`: Start Dagster dev server.
*   `make test`: Run dbt tests and Python unit tests.
*   `make clean`: Clean up artifacts.
