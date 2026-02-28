# Retail Analytics Platform - Architecture & Implementation

## Architecture Overview

The project is split into two distinct components to mimic a production environment:

1.  **Ingestion Simulator (`ingestion_simulator/`)**:
    *   **Role**: Simulates external data sources (CDC, Third-party APIs).
    *   **Mechanism**: Generates synthetic data (Customers, Products, Orders) and pushes it directly to StarRocks using **Stream Load**.
    *   **Infrastructure**: Runs as a standalone CLI tool or container.

2.  **Transformation Pipeline (`transformation_pipeline/`)**:
    *   **Role**: The core data platform logic (Dagster + dbt).
    *   **Mechanism**:
        *   **Observe**: Polls StarRocks `raw_` tables for changes (row counts) via `check_sources_job`.
        *   **Trigger**: Uses `AutomationConditionSensor` to auto-materialize downstream assets.
        *   **Transform**: `raw` -> `staging` (Clean) -> `marts` (Star Schema).
    *   **Deployment**: Ready for K8s/Cloud deployment.

## Key Features Implemented

*   **Decoupled Architecture**: Ingestion and Transformation are loosely coupled via the Data Warehouse (StarRocks).
*   **High-Performance Ingestion**: **Stream Load** (JSON) handles high throughput directly into OLAP.
*   **Automated Orchestration**:
    *   **Observable Source Assets**: Dagster is aware of external data changes.
    *   **Auto-Materialization**: Reactive pipeline execution without strict schedules.
*   **Modern Developer Experience**:
    *   **Monorepo**: Unified `Makefile` and `uv` workspace.
    *   **Docker**: Reproducible StarRocks environment.
    *   **dbt**: Best-practice dimensional modeling.

## Next Steps

*   **Deployment**: Deploy `transformation_pipeline` to Kubernetes using Luban CI.
*   **Incremental Models**: Optimize `fact_daily_sales` to use incremental strategy for large datasets.
*   **BI Integration**: Connect Apache Superset or Metabase to StarRocks for visualization.
*   **Data Contracts**: Implement stricter schema enforcement at the ingestion layer.
