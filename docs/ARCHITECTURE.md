# Architecture & Design Principles

This document outlines the architectural decisions and design patterns used in the Retail Analytics Platform. It is intended to guide engineers in understanding the "Why" behind the implementation.

## 1. High-Level Architecture: The Modern Data Stack

The platform is built on three core pillars:
1.  **Orchestration & Observation**: Dagster
2.  **Transformation**: dbt (Data Build Tool)
3.  **Compute & Storage**: StarRocks (OLAP Database)

### Why this stack?

*   **StarRocks**: A high-performance, real-time analytical database. Unlike traditional warehouses (Snowflake/BigQuery), it excels at low-latency queries and supports efficient upserts (Primary Key model), making it ideal for operational analytics.
*   **dbt**: The industry standard for data transformation. It brings software engineering practices (version control, testing, modularity) to SQL.
*   **Dagster**: A data-aware orchestrator. Unlike Airflow (which orchestrates *tasks*), Dagster orchestrates *assets* (tables, files, ML models). It understands the data dependencies and provides built-in lineage, observability, and data quality checks.

## 2. The Decoupled Monorepo Pattern

We use a **monorepo** structure (`dagster-example/`) that houses multiple distinct **projects** (or "code locations" in Dagster terminology). This mimics a real-world enterprise environment where different teams manage different parts of the data estate.

### The "Producer-Consumer" Model (Data Mesh)

*   **Master Data (`master_data/`)**: The **Producer**.
    *   **Responsibility**: Owns shared, foundational dimensions that are used across the organization (e.g., `dim_date`, `dim_geography`).
    *   **Output**: Publishes high-quality, governable tables to the `master_data` schema.
    *   **Contract**: Downstream teams can rely on these tables but cannot modify them.

*   **Transformation Pipeline (`transformation_pipeline/`)**: The **Consumer**.
    *   **Responsibility**: Owns the domain-specific analytics for the Retail business unit.
    *   **Input**: Consumes raw data (`raw_orders`) and shared dimensions (`master_data.dim_date`).
    *   **Output**: Produces domain-specific marts (`fact_daily_sales`, `dim_customers`).

### Benefits
*   **Isolation**: Changes in the analytics pipeline cannot break the master data generation.
*   **Scalability**: New teams (e.g., "Marketing", "Finance") can add their own projects without touching existing code.
*   **Clear Ownership**: Code locations define clear boundaries of responsibility.

## 3. Engineering Practices

### Environment Management (`uv`)
We use `uv` for Python package management. Each project (`master_data`, `transformation_pipeline`) has its own `pyproject.toml` and `.venv`.
*   **Why?**: Prevents dependency conflicts. One project might need `pandas==1.5` while another needs `pandas==2.0`. Dagster's `workspace.yaml` supports loading from different environments seamlessly.

### Infrastructure as Code (Docker & Make)
*   **Docker Compose**: Defines the entire infrastructure (StarRocks FE/BE) in code.
*   **Makefiles**: Abstract complex commands. `make setup` creates a reproducible environment for any developer, anywhere.

### Configuration Management
*   **Environment Variables (`.env`)**: Secrets (passwords) and environment-specific configs (hostnames) are never committed.
*   **Profiles (`profiles.yml`)**: dbt connection settings are managed via profiles that read from env vars, supporting `development`, `staging`, and `production` targets dynamically.
