
from dagster import observable_source_asset, AssetKey, AssetExecutionContext, DataVersion, ObserveResult
from retail_analytics.resources.starrocks import StarRocksResource
import pandas as pd
from sqlalchemy.exc import ProgrammingError

# Helper to check row count
def get_row_count(context: AssetExecutionContext, starrocks: StarRocksResource, table_name: str) -> int:
    try:
        query = f"SELECT COUNT(*) as cnt FROM {table_name}"
        df = starrocks.execute_query(query)
        if not df.empty:
            return int(df['cnt'][0])
        return 0
    except ProgrammingError as e:
        # Table might not exist yet if reset-db just ran or DB is empty
        # 1146 is MySQL error code for "Table doesn't exist"
        if "1146" in str(e):
            context.log.warning(f"Table {table_name} does not exist yet. Returning count 0.")
            return 0
        context.log.error(f"SQL Error checking {table_name}: {e}")
        raise e
    except Exception as e:
        context.log.error(f"Unexpected error checking {table_name}: {e}")
        # In observation, we might want to return 0 to avoid crashing the sensor, 
        # but logging the error is crucial.
        return 0

@observable_source_asset(key=AssetKey("raw_orders"), description="Raw orders table", group_name="raw")
def raw_orders(context: AssetExecutionContext, starrocks: StarRocksResource):
    count = get_row_count(context, starrocks, "raw_orders")
    return ObserveResult(data_version=DataVersion(str(count)), metadata={"row_count": count})

@observable_source_asset(key=AssetKey("raw_customers"), description="Raw customers table", group_name="raw")
def raw_customers(context: AssetExecutionContext, starrocks: StarRocksResource):
    count = get_row_count(context, starrocks, "raw_customers")
    return ObserveResult(data_version=DataVersion(str(count)), metadata={"row_count": count})

@observable_source_asset(key=AssetKey("raw_products"), description="Raw products table", group_name="raw")
def raw_products(context: AssetExecutionContext, starrocks: StarRocksResource):
    count = get_row_count(context, starrocks, "raw_products")
    return ObserveResult(data_version=DataVersion(str(count)), metadata={"row_count": count})
