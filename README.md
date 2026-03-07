# Retail Analytics Platform

A realistic data platform built with **Dagster**, **dbt**, and **StarRocks**.

## Architecture

This project follows a decoupled monorepo architecture:

1.  **Ingestion Simulator** (`ingestion_simulator/`):
    *   A standalone Python CLI tool (`ingest`).
    *   Generates mock retail data (Customers, Products, Orders).
    *   Ingests data directly into StarRocks using **Stream Load**.
    *   Manages database lifecycle (Init, Reset).

2.  **Master Data Management** (`master_data/`):
    *   A centralized producer of shared dimensions (e.g., `dim_date`).
    *   Publishes reference data to the `master_data` schema.
    *   Ensures consistency across the platform.

3.  **Retail Analytics** (`retail_analytics/`):
    *   A Dagster project managing the analytics lifecycle.
    *   Consumes raw data and shared dimensions to build data marts.
    *   **dbt** models transform data (`stg_*` -> `fact_sales`).
    *   Dagster assets observe StarRocks tables and trigger dbt runs.

## Prerequisites

*   Python 3.12+
*   Docker & Docker Compose
*   `uv` (Package Manager) - [Install uv](https://github.com/astral-sh/uv)

## Quick Start

1.  **Configure**:
    Create and configure the `.env` file.
    ```bash
    make create-env
    ```
    *   **Remote/JupyterHub Users**: Open `.env` and set `STARROCKS_HOST` to your remote database IP.
    *   **Local Users**: No changes needed (defaults to `127.0.0.1`).

2.  **Setup Environment**:
    Install dependencies, start StarRocks (if local), and initialize the database.
    ```bash
    make setup
    ```

3.  **Start Dagster**:
    Launch the Dagster UI (available at http://localhost:3000).
    ```bash
    make dev
    ```

4.  **Generate Data**:
    In a new terminal, generate mock data and load it into StarRocks.
    ```bash
    make generate
    ```
    You will see logs indicating successful Stream Load.

5.  **Observe & Transform**:
    *   Go to Dagster UI (Overview > Jobs).
    *   The `check_sources_job` runs every minute to detect new data.
    *   Once data is detected, the `default_automation_condition_sensor` will automatically trigger the dbt models (`stg_*` -> `dim_*`, `fact_*`).
    *   You can also manually materialize assets if you prefer.

6.  **Remote Development (JupyterHub)**:
    This project supports remote development where StarRocks is hosted externally (e.g., in a shared Kubernetes cluster).
    *   **Configuration**: Set `STARROCKS_HOST` in `.env` to your remote IP/hostname (anything other than `127.0.0.1` or `localhost`).
    *   **Smart Setup**: `make setup` will automatically detect the remote host and **skip** Docker container startup, while still initializing the database tables.
    *   **Safety**: `make reset-db` will prompt for confirmation before dropping tables on a remote database.

## Documentation

For a deeper dive into the engineering decisions and architecture:

*   [**Architecture & Design Principles**](docs/ARCHITECTURE.md): The "Why" behind the stack (StarRocks, Data Mesh, Monorepo).
*   [**Dagster & dbt Integration Guide**](docs/DAGSTER_DBT_INTEGRATION.md): How orchestration and transformation work together seamlessly.
*   [**Master Data Strategy**](docs/MASTER_DATA_STRATEGY.md): Deep dive into Shared Dimensions and the high-performance Date Generator.
*   [**Ingestion Simulator**](docs/INGESTION_SIMULATOR.md): Simulating real-time data streams with StarRocks Stream Load.

## Project Structure

*   `ingestion_simulator/`: Data generation tool.
    *   `src/`: Python source code.
    *   `Makefile`: Simulator-specific commands.
*   `master_data/`: Shared dimensions (Producer).
    *   `src/master_data/`: Dagster assets.
    *   `dbt_project/`: dbt models (e.g., `dim_date`).
*   `retail_analytics/`: Analytics pipeline (Consumer).
    *   `src/retail_analytics/`: Dagster assets and definitions.
    *   `dbt_project/`: dbt models and tests.
*   `dagster_home/`: Local Dagster storage (logs, run history).
*   `docker-compose.yml`: Infrastructure (StarRocks).
*   `Makefile`: Root orchestrator.

## Commands

*   `make setup`: Full setup (install, check-env, infra-check, init-db).
*   `make create-env`: Create configuration file from template.
*   `make install`: Install Python dependencies (using `uv`).
*   `make up`: Start StarRocks containers (Local only).
*   `make down`: Stop containers (Local only).
*   `make init-db`: Initialize StarRocks database/tables.
*   `make reset-db`: Reset database (DROP/CREATE) and re-run dbt models (Prompts if remote).
*   `make generate`: Generate and load mock data.
*   `make dev`: Start Dagster dev server.
*   `make test`: Run dbt tests and Python unit tests.
*   `make dbt-deps`: Install dbt packages.
*   `make clean`: Clean up artifacts.
*   `make help`: Show available commands.
