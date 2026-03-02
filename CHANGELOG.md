# Changelog

All notable changes to the Retail Analytics Platform will be documented in this file.

## [0.2.0] - 2026-03-02

### Added
- **Master Data Management**: Introduced `master_data` project for shared dimensions (`dim_date`).
- **Documentation Suite**: Added comprehensive architectural docs in `docs/`:
    - `ARCHITECTURE.md`: High-level design and Data Mesh principles.
    - `DAGSTER_DBT_INTEGRATION.md`: Explanation of asset-based orchestration.
    - `MASTER_DATA_STRATEGY.md`: Details on `dim_date` generation algorithm.
    - `INGESTION_SIMULATOR.md`: Guide to real-time data simulation.
- **Robust Infrastructure**:
    - Added `dagster_home` persistence configuration.
    - Increased StarRocks FE memory limit (4GB) to prevent OOM/GC issues.
    - Improved `make setup` reliability with backend health checks.

### Changed
- **Data Modeling Standards**:
    - Renamed dimensions to Singular (`dim_customers` -> `dim_customer`, `dim_products` -> `dim_product`).
    - Kept facts Plural (`fact_daily_sales`).
- **Configuration**:
    - Updated `schema.yml` to use modern dbt syntax (nested `arguments` for generic tests).
    - Moved `DAGSTER_HOME` configuration to `Makefile` to ensure absolute path handling.
- **CLI Tooling**:
    - Evaluated `dg` CLI but decided to stick with `dagster dev` for robust monorepo/venv isolation.

### Fixed
- Fixed `dagster_home` absolute path error in `Makefile`.
- Fixed `dbt parse` warnings regarding deprecated test syntax.
- Fixed StarRocks startup race conditions in Docker Compose.
