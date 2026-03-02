# Retail Analytics

This directory contains the Dagster and dbt projects for the Retail Analytics Platform. It is responsible for consuming raw data, transforming it into analytics-ready models, and orchestrating the process.

See the root [README.md](../README.md) for full setup instructions.

## Structure

*   `src/retail_analytics/`: Dagster definitions, resources, and sensors.
*   `dbt_project/`: dbt models (Staging, Marts) and tests.
*   `tests/`: Python unit tests.
*   `Makefile`: Local development commands for the pipeline.

## Data Models

The pipeline transforms raw data into a Star Schema optimized for analytics:

### Dimensional Models (`dim_*`)
*   **`dim_customer`**: Enriched customer profiles (from `raw_customers`).
*   **`dim_product`**: Product catalog details (from `raw_products`).

### Fact Models (`fact_*`)
*   **`fact_daily_sales`**: An incremental table that aggregates sales metrics (Revenue, Quantity, Order Count).
    *   **Grain**: Daily per Product per Order Status.
    *   **Strategy**: `microbatch` incremental loading (processing data day-by-day).
    *   **Partitions**: Partitioned by `order_date` for efficient querying in StarRocks.

## Development

Run commands inside `retail_analytics/` (via `make -C retail_analytics` or `cd retail_analytics`):

*   `make dev`: Start Dagster dev server.
*   `make dbt-deps`: Install dbt packages (e.g., dbt-utils).
*   `make dbt-parse`: Generate `manifest.json` for Dagster.
*   `uv run dbt build`: Run all dbt models and tests.
