# Changelog

All notable changes to the Retail Analytics Platform will be documented in this file.

## [0.3.1] - 2026-03-03

### Infrastructure & DevEx
- **Smart Makefile**: Added auto-detection for Local vs. Remote (`STARROCKS_HOST`) environments.
    - `make setup` skips Docker startup if connecting to a remote database (e.g., JupyterHub).
    - `make reset-db` prompts for confirmation when running against a remote database.
- **Webserver Config**: Added `DAGSTER_WEBSERVER_HOST` and `DAGSTER_WEBSERVER_PORT` support in `.env` (defaulting to `0.0.0.0:3000`).

### Fixed
- **Robustness**: Patched `dbt_assets.py` to ignore internal `checkpoint` events from dbt adapters, preventing crashes during incremental runs.

## [0.3.0] - 2026-03-03

### Refactoring & Optimization
- **Project Structure**: Renamed `transformation_pipeline` to `retail_analytics` and adopted the standard `src/` layout for improved packaging and import resolution.
- **dbt Logic**: Optimized incremental models (`stg_orders`, `dim_customer`) to use StarRocks primary keys instead of inefficient anti-joins.
- **Configuration**: Extracted hardcoded constants in `ingestion_simulator` to `config.py`.
- **Code Quality**: Refactored `get_row_count` in `source_assets.py` for robust error handling and logging.

### Added
- **Observability**: Source assets now emit `row_count` metadata for trend tracking in Dagster UI.
- **Asset Grouping**: dbt assets are now automatically grouped into `staging` and `marts` in the UI lineage graph.
- **Testing**: Added `retail_analytics/tests/test_definitions.py` smoke test for definition integrity.
- **Master Data**: Added `AutomationConditionSensor` to `master_data` for consistency.

### Fixed
- Fixed `dagster_project` import errors in `source_assets.py`.
- Fixed `DBT_PROJECT_DIR` path resolution in `dbt_assets.py`.
- Fixed SQL syntax documentation in `MASTER_DATA_STRATEGY.md` and `master_data/README.md`.
- Added missing `DROP TABLE` hook for `stg_order_items` in `dbt_project.yml`.

## [0.2.0] - 2026-03-02

### Added
- Added dbt models: `stg_*`, `dim_customer`, `dim_product`, `fact_daily_sales`.
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
