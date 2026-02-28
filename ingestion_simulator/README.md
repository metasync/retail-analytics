# Ingestion Simulator

A standalone Python CLI tool for generating mock retail data and ingesting it into StarRocks using Stream Load.

## Features

*   **Mock Data Generation**: Uses `faker` to generate Customers, Products, and Orders.
*   **Direct Ingestion**: Stream Loads data directly into StarRocks (JSON format).
*   **Database Management**: Initialize and reset database schema (`raw_` tables).
*   **Local & Docker Support**: Automatically handles redirect rewriting for local development (rewrites internal Docker IPs to localhost).

## Installation

This project is managed by `uv`.

```bash
cd ingestion_simulator
uv sync
```

## Configuration

Copy `.env.example` to `.env` (or rely on the root `.env` if running from root Makefile):

```bash
cp .env.example .env
```

Key variables:
*   `STARROCKS_HOST`: Hostname (default: `127.0.0.1` locally, `starrocks-fe` in Docker).
*   `STARROCKS_HTTP_PORT`: FE HTTP Port (default: `18030` locally).
*   `STARROCKS_DB`: Database name (default: `retail_development`).

## Usage

Run the CLI using `uv run ingest`.

### 1. Initialize Database
Create the database and tables (`raw_orders`, `raw_customers`, `raw_products`).

```bash
uv run ingest starrocks init
```

### 2. Reset Database
Drop all tables and recreate them (useful for clean slate).

```bash
uv run ingest starrocks reset
```

### 3. Generate Data
Generate mock data and load it.

```bash
# Default (10 customers, 20 products, 15 orders)
uv run ingest data generate

# Custom volume
uv run ingest data generate --customers 100 --products 50 --orders 200

# Via Makefile
make generate ARGS="--customers 100 --products 50 --orders 200"
```

## Architecture

*   `src/ingestion_simulator/`: Package source.
    *   `cli.py`: Entry point (`click`).
    *   `generator.py`: Data generation and Stream Load logic.
    *   `starrocks.py`: Schema management (SQLAlchemy).
    *   `config.py`: Configuration loading.
