# dbt Project

This dbt project transforms raw data loaded into StarRocks into a dimensional model (Star Schema) suitable for analytics.

## Architecture

The project follows a standard 2-layer architecture:

1.  **Staging** (`models/staging/`):
    *   One-to-one mapping with raw tables (`raw_orders`, `raw_customers`, `raw_products`).
    *   Performs light cleaning, type casting, and column renaming.
    *   Materialized as tables (or views) in StarRocks.

2.  **Marts** (`models/marts/`):
    *   **Dimensions**:
        *   `dim_customers`: Enriched customer data.
        *   `dim_products`: Product details.
    *   **Facts**:
        *   `fact_daily_sales`: Daily aggregated sales metrics (total revenue, order count) by product and status.

## Data Lineage

`raw_*` (Sources) -> `stg_*` (Staging) -> `dim_*` / `fact_*` (Marts)

## Running dbt

This project is managed by `uv`.

```bash
# Install dependencies (e.g. dbt-utils)
uv run dbt deps

# Run all models and tests
uv run dbt build

# Generate documentation
uv run dbt docs generate
uv run dbt docs serve
```

## Testing

Data quality tests are defined in `schema.yml` files.
*   **Unique & Not Null**: Primary keys.
*   **Relationships**: Foreign key integrity.
*   **Accepted Values**: Enum checks (e.g., order status).
