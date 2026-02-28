
import click
from ingestion_simulator.starrocks import wait_for_connection, init_database, create_tables, reset_tables
from ingestion_simulator.generator import generate_customers, generate_products, generate_orders, stream_load

@click.group()
def cli():
    """Ingestion Simulator CLI"""
    pass

@cli.group()
def starrocks():
    """Manage StarRocks database."""
    pass

@starrocks.command("init")
def starrocks_init():
    """Initialize StarRocks database and tables."""
    wait_for_connection()
    init_database()
    create_tables()

@starrocks.command("reset")
def starrocks_reset():
    """Reset StarRocks tables (DROP and CREATE)."""
    wait_for_connection()
    init_database()
    reset_tables()

@cli.group()
def data():
    """Generate and ingest mock data."""
    pass

@data.command("generate")
@click.option("--customers", default=10, help="Number of customers")
@click.option("--products", default=20, help="Number of products")
@click.option("--orders", default=15, help="Number of orders")
def data_generate(customers, products, orders):
    """Generate mock data and stream load to StarRocks."""
    print(f"Generating {customers} customers, {products} products, {orders} orders...")
    
    c_list = generate_customers(customers)
    stream_load("raw_customers", c_list)
    
    p_list = generate_products(products)
    stream_load("raw_products", p_list)
    
    o_list = generate_orders(c_list, p_list, orders)
    stream_load("raw_orders", o_list)

if __name__ == "__main__":
    cli()
