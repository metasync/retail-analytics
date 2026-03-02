# Master Data Management

This project manages shared dimensional data (e.g., `dim_date`) for the Retail Analytics platform. It serves as a central "Producer" of reference data that other pipelines (like `retail_analytics`) consume.

It includes:
- **dbt Project**: Defines the SQL logic for dimensions.
- **Dagster Project** (`src/master_data`): Orchestrates the dbt models and exposes them as assets.

## Development

Run commands inside `master_data/` (via `make -C master_data` or `cd master_data`):

*   `make dev`: Start Dagster dev server (for this project only).
*   `make dbt-deps`: Install dbt packages.
*   `make dbt-build`: Build dimensions (e.g., populate `dim_date`).
*   `uv run dbt run`: Run specific models.

## Technical Implementation Details

### Date Dimension Generation (`dim_date`)

The `dim_date` model uses a high-performance "Numbers Table" CTE approach instead of standard recursion or database-specific functions. This ensures compatibility with StarRocks (and any SQL database) while remaining extremely fast.

**Algorithm Explanation:**

1.  **Digits CTE**: We start by creating a simple Common Table Expression (CTE) containing the digits 0 through 9.
2.  **Cross Join Generation**: We cross-join this set of digits with itself 4 times.
    *   `digits` (ones) × `digits` (tens) × `digits` (hundreds) × `digits` (thousands)
    *   This generates $10^4 = 10,000$ unique combinations.
3.  **Number Calculation**: For each row, we calculate the integer value:
    $$ \text{num} = d_1 + (d_2 \times 10) + (d_3 \times 100) + (d_4 \times 1000) $$
    This produces a seamless sequence of integers from 0 to 9,999.
4.  **Date Projection**: We treat these integers as "days offset from the start date".
    *   `date_day = '2020-01-01' + num days`
    *   This allows us to generate ~27 years of daily records instantly.

```sql
with digits as (
    select 0 as d union all select 1 ... select 9
),
numbers as (
    -- Cross join to generate 0-9999
    select d1.d + (d2.d * 10) + (d3.d * 100) + (d4.d * 1000) as num
    from digits d1
    cross join digits d2
    cross join digits d3
    cross join digits d4
),
dates as (
    select date_add('2020-01-01', interval num day) as date_day
    from numbers
)
```

**Why this approach?**
*   **Performance**: Columnar databases like StarRocks are heavily optimized for cross-joins. Generating 10,000 rows this way is virtually instantaneous compared to recursive loops.
*   **Compatibility**: It avoids database-specific syntax like `GENERATE_SERIES` (Postgres) or `WITH RECURSIVE` quirks (which can vary by DB version or require special flags).
