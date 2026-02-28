# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-03-01

### Architecture
- **Decoupled Monorepo**: Split project into `ingestion_simulator` (standalone CLI) and `transformation_pipeline` (Dagster + dbt).
- **Stream Load Ingestion**: Replaced file-based ingestion (MinIO) with direct HTTP Stream Load into StarRocks for higher performance.
- **Removed MinIO**: Simplified infrastructure by removing MinIO and S3 dependencies.
- **Removed DuckDB**: Standardized on StarRocks as the single source of truth (Data Warehouse).

### Ingestion Simulator
- **New CLI Tool**: Introduced `ingest` CLI managed by `uv`.
- **Features**:
    - `starrocks init/reset`: Manage DB lifecycle.
    - `data generate`: High-performance synthetic data generation.
- **Local Dev Support**: Automatic port rewriting for local Docker environments (redirecting internal IPs).

### Transformation Pipeline
- **Observable Source Assets**: Implemented polling mechanism (`check_sources_job`) to detect data changes in StarRocks.
- **Auto-Materialization**: Enabled `AutomationConditionSensor` to trigger dbt models automatically upon data arrival.
- **dbt Integration**:
    - Updated `dbt-starrocks` adapter configuration.
    - Implemented clean Staging -> Marts lineage.
    - Added `dbt-utils` for robust modeling.

### Developer Experience
- **Tooling**: Migrated entire project to `uv` for fast, reliable dependency management.
- **Makefiles**: Unified `Makefile` commands for setup, dev, and generation.
- **Documentation**:
    - Updated `README.md` (Root, Ingestion, Transformation, dbt).
    - Refreshed `REQUIREMENTS.md` and `PLAN.md`.
- **Cleanup**: Removed unused dependencies (`pandera`, `pyarrow`) and legacy assets (`lake_assets.py`).

### Fixes
- Fixed `dagster dev` startup by ensuring `manifest.json` generation.
- Fixed Python package discovery for `retail-analytics`.
- Fixed `docker-compose` health checks and dependencies.
