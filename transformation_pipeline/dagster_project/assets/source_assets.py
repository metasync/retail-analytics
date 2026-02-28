
from dagster import observable_source_asset, AssetKey, AssetExecutionContext, DataVersion
from dagster_project.resources.starrocks import StarRocksResource
import pandas as pd

# Helper to check row count
def get_row_count(starrocks: StarRocksResource, table_name: str) -> int:
    try:
        query = f"SELECT COUNT(*) as cnt FROM {table_name}"
        df = starrocks.execute_query(query)
        if not df.empty:
            return int(df['cnt'][0])
        return 0
    except Exception as e:
        # Table might not exist yet if reset-db just ran
        return 0

@observable_source_asset(key=AssetKey("raw_orders"), description="Raw orders table")
def raw_orders(context: AssetExecutionContext, starrocks: StarRocksResource):
    count = get_row_count(starrocks, "raw_orders")
    return DataVersion(str(count))

@observable_source_asset(key=AssetKey("raw_customers"), description="Raw customers table")
def raw_customers(context: AssetExecutionContext, starrocks: StarRocksResource):
    count = get_row_count(starrocks, "raw_customers")
    return DataVersion(str(count))

@observable_source_asset(key=AssetKey("raw_products"), description="Raw products table")
def raw_products(context: AssetExecutionContext, starrocks: StarRocksResource):
    count = get_row_count(starrocks, "raw_products")
    return DataVersion(str(count))
