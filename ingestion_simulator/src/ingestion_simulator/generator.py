
import json
import random
import requests
import os
import sys
from urllib.parse import urlparse, urlunparse
from datetime import datetime
from faker import Faker
from ingestion_simulator.config import STARROCKS_HOST, STARROCKS_HTTP_PORT, STARROCKS_DB, get_auth

fake = Faker()

# Constants
PRODUCT_CATEGORIES = ["Electronics", "Clothing", "Home", "Books", "Sports"]
ORDER_STATUSES = ["PENDING", "COMPLETED", "SHIPPED", "CANCELLED"]
STARROCKS_BE_HTTP_PORT = int(os.getenv("STARROCKS_BE_HTTP_PORT", "18040"))

def stream_load(table, data):
    url = f"http://{STARROCKS_HOST}:{STARROCKS_HTTP_PORT}/api/{STARROCKS_DB}/{table}/_stream_load"
    
    headers = {
        "format": "json",
        "strip_outer_array": "true",
        "ignore_json_size": "true",
        "Expect": "100-continue"
    }
    
    json_data = json.dumps(data)
    
    print(f"Loading {len(data)} records into {table} via Stream Load...")
    
    try:
        response = requests.put(
            url, 
            data=json_data, 
            headers=headers,
            auth=get_auth(),
            allow_redirects=False
        )
        
        if response.status_code == 307:
            redirect_url = response.headers['Location']
            
            # Local Dev: StarRocks BE returns internal IP/Port (8040). 
            # If we are on localhost, we must rewrite to localhost:18040 (or configured port).
            if STARROCKS_HOST in ["127.0.0.1", "localhost"]:
                parsed = urlparse(redirect_url)
                if parsed.port == 8040:
                    # Replace internal IP/Port with localhost:STARROCKS_BE_HTTP_PORT
                    new_netloc = f"127.0.0.1:{STARROCKS_BE_HTTP_PORT}"
                    redirect_url = urlunparse(parsed._replace(netloc=new_netloc))
            
            response = requests.put(
                redirect_url,
                data=json_data,
                headers=headers,
                auth=get_auth()
            )
            
        res = response.json()
        if res.get("Status") == "Success":
            print(f"Success: {res.get('NumberLoadedRows')} rows loaded.")
        else:
            print(f"Failed: {res}")
            print(f"Error URL: {res.get('ErrorURL')}")
            # Raise exception to ensure CLI fails
            raise Exception(f"Stream Load Failed: {res.get('Message')}")

    except Exception as e:
        print(f"Stream Load Exception: {e}")
        # Re-raise to propagate failure
        raise

def generate_customers(num_customers=5):
    customers = []
    for _ in range(num_customers):
        customer = {
            "customer_id": fake.uuid4(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "city": fake.city(),
            "country": fake.country(),
            "created_at": datetime.now().isoformat()
        }
        customers.append(customer)
    return customers

def generate_products(num_products=10):
    products = []
    for _ in range(num_products):
        product = {
            "product_id": fake.uuid4(),
            "name": fake.bs(),
            "category": random.choice(PRODUCT_CATEGORIES),
            "price": round(random.uniform(10.0, 1000.0), 2),
            "updated_at": datetime.now().isoformat()
        }
        products.append(product)
    return products

def generate_orders(customers, products, num_orders=20):
    orders = []
    for _ in range(num_orders):
        customer = random.choice(customers)
        
        num_items = random.randint(1, 5)
        items = []
        total_amount = 0.0

        for _ in range(num_items):
            product = random.choice(products)
            quantity = random.randint(1, 3)
            price = product["price"]
            
            items.append({
                "product_id": product["product_id"],
                "quantity": quantity,
                "price": price
            })
            total_amount += price * quantity

        order = {
            "order_id": fake.uuid4(),
            "customer_id": customer["customer_id"],
            "order_date": datetime.now().isoformat(),
            "status": random.choice(ORDER_STATUSES),
            "total_amount": round(total_amount, 2),
            "items": json.dumps(items) # Serialize items as JSON string for StarRocks JSON type
        }
        orders.append(order)
    return orders
