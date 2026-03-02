# Ingestion Simulator

Real-world data platforms don't just query static CSVs; they handle continuous streams of data from operational systems (Orders, Clicks, IoT). The **Ingestion Simulator** is designed to mimic this "Real-Time" or "Micro-batch" data flow.

## 1. Role in the Architecture

The simulator acts as a proxy for your upstream operational systems (e.g., Shopify, Salesforce, or a Kafka topic).
*   It generates synthetic, relational data (Customers, Products, Orders).
*   It pushes this data directly into the **Raw Layer** of the data warehouse (StarRocks).

## 2. Technical Implementation

### Data Generation (`Faker`)
We use the Python `faker` library to generate realistic, semantically valid data.
*   **Determinism**: We can seed the generator to produce reproducible datasets for testing.
*   **Relational Integrity**: The simulator ensures that an `Order` references a valid `Customer` and `Product` that it just created (or previously created).

### Ingestion Method: Stream Load
Instead of standard SQL `INSERT` statements, we use **StarRocks Stream Load**.

**Why Stream Load?**
*   **Performance**: `INSERT INTO values (...)` is transactional and slow for large volumes. Stream Load streams CSV/JSON data directly into memory and flushes it to disk in batches. It is designed for millions of events per second.
*   **Atomicity**: Each load is a transaction. Either the whole batch succeeds, or it fails.
*   **JSON Support**: We generate Python dictionaries and stream them as JSON lines, which is a common format for modern event buses (like Kafka/Redpanda).

### The "Raw Layer" Pattern
The simulator writes to tables prefixed with `raw_` (`raw_orders`, `raw_customers`).
*   **Schema**: These tables use `DUPLICATE KEY` (in StarRocks) to allow appending all events, even duplicates or updates.
*   **Philosophy**: "Capture everything, transform later." We do not apply business logic here.
*   **ELT (Extract, Load, Transform)**: The simulator handles **EL**, and dbt handles **T**.

## 3. Simulation Workflow

1.  **`make init-db`**: Creates the `raw_` tables in StarRocks.
2.  **`make generate`**:
    *   Generates a batch of Customers.
    *   Generates a batch of Products.
    *   Generates Orders linking the above.
    *   Streams them to StarRocks via HTTP (Stream Load).
3.  **Dagster Observation**:
    *   The `check_sources_job` (running every minute) detects that the `raw_orders` table has been updated (via row count or max timestamp).
    *   This triggers the downstream dbt pipeline.

This creates a realistic **Event-Driven Architecture**: You generate data, and the pipeline automatically wakes up to process it.
