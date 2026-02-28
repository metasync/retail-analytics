
import time
from sqlalchemy import create_engine, text
from ingestion_simulator.config import get_mysql_connection_string, STARROCKS_DB

def wait_for_connection(max_retries=30):
    print(f"Waiting for StarRocks...")
    engine = create_engine(get_mysql_connection_string("information_schema"))
    
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Connected to StarRocks!")
            return
        except Exception as e:
            print(f"Waiting... ({i+1}/{max_retries})")
            time.sleep(2)
    raise Exception("Could not connect to StarRocks")

def init_database():
    engine = create_engine(get_mysql_connection_string("information_schema"))
    with engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {STARROCKS_DB}"))
    print(f"Database {STARROCKS_DB} ready.")

def create_tables():
    engine = create_engine(get_mysql_connection_string())
    with engine.connect() as conn:
        # Raw Orders
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_orders (
                order_id STRING,
                customer_id STRING,
                order_date DATETIME,
                status STRING,
                total_amount DOUBLE,
                items JSON
            )
            ENGINE=OLAP
            DUPLICATE KEY(order_id)
            DISTRIBUTED BY HASH(order_id) BUCKETS 1
            PROPERTIES ("replication_num" = "1");
        """))
        
        # Raw Customers
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_customers (
                customer_id STRING,
                first_name STRING,
                last_name STRING,
                email STRING,
                city STRING,
                country STRING,
                created_at DATETIME
            )
            ENGINE=OLAP
            DUPLICATE KEY(customer_id)
            DISTRIBUTED BY HASH(customer_id) BUCKETS 1
            PROPERTIES ("replication_num" = "1");
        """))
        
        # Raw Products
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS raw_products (
                product_id STRING,
                name STRING,
                category STRING,
                price DOUBLE,
                updated_at DATETIME
            )
            ENGINE=OLAP
            DUPLICATE KEY(product_id)
            DISTRIBUTED BY HASH(product_id) BUCKETS 1
            PROPERTIES ("replication_num" = "1");
        """))
    print("Tables created.")

def reset_tables():
    engine = create_engine(get_mysql_connection_string())
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS raw_orders FORCE"))
        conn.execute(text("DROP TABLE IF EXISTS raw_customers FORCE"))
        conn.execute(text("DROP TABLE IF EXISTS raw_products FORCE"))
    print("Tables dropped.")
    create_tables()
