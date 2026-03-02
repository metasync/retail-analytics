
# Retail Analytics Platform - Architecture & Implementation

## Architecture Overview

The project is split into three distinct components to mimic a production environment:

1.  **Ingestion Simulator (`ingestion_simulator/`)**:
    *   **Role**: Simulates external data sources (CDC, Third-party APIs).
    *   **Mechanism**: Generates synthetic data (Customers, Products, Orders) and pushes it directly to StarRocks using **Stream Load**.
    *   **Infrastructure**: Runs as a standalone CLI tool or container.

2.  **Retail Analytics (`retail_analytics/`)**:
    *   **Role**: The core data platform logic (Dagster + dbt).
    *   **Mechanism**:
        *   **Observe**: Polls StarRocks `raw_` tables for changes (row counts) via `check_sources_job`.
        *   **Trigger**: Uses `AutomationConditionSensor` to auto-materialize downstream assets.
        *   **Transform**: `raw` -> `staging` (Clean) -> `marts` (Star Schema).
    *   **Deployment**: Ready for K8s/Cloud deployment.

3.  **Master Data Management (`master_data/`)**:
    *   **Role**: Centralized producer of shared dimensions (e.g., `dim_date`).
    *   **Mechanism**:
        *   **Generate**: Uses efficient SQL cross-joins to generate date dimension.
        *   **Publish**: Exposes read-only tables for other pipelines to consume.
    *   **Benefit**: Ensures consistency across the platform.

## Implementation Status

- [x] **Decoupled Architecture**: Ingestion and Transformation are loosely coupled via the Data Warehouse (StarRocks).
- [x] **High-Performance Ingestion**: **Stream Load** (JSON) handles high throughput directly into OLAP.
- [x] **Automated Orchestration**:
    - [x] **Observable Source Assets**: Dagster is aware of external data changes.
    - [x] **Auto-Materialization**: Reactive pipeline execution without strict schedules.
- [x] **Modern Developer Experience**:
    - [x] **Monorepo**: Unified `Makefile` and `uv` workspace.
    - [x] **Docker**: Reproducible StarRocks environment.
    - [x] **dbt**: Best-practice dimensional modeling.
- [x] **Incremental Models**: Optimized `fact_daily_sales` and `dim_customer` using StarRocks primary keys.
- [x] **Refactoring**: Standardized project structure (`src/` layout) and optimized configuration.

## Next Steps

*   **Deployment**: Deploy `retail_analytics` to Kubernetes using Luban CI.
*   **BI Integration**: Connect Apache Superset or Metabase to StarRocks for visualization.
*   **Data Contracts**: Implement stricter schema enforcement at the ingestion layer.
*   **Advanced Testing**: Add integration tests running against a real StarRocks instance in CI.
