
import os
from dotenv import load_dotenv

load_dotenv()

STARROCKS_HOST = os.getenv("STARROCKS_HOST", "127.0.0.1")
STARROCKS_PORT = int(os.getenv("STARROCKS_PORT", "19030")) # FE Query Port
STARROCKS_HTTP_PORT = int(os.getenv("STARROCKS_HTTP_PORT", "8030")) # FE HTTP Port
STARROCKS_USER = os.getenv("STARROCKS_USER", "root")
STARROCKS_PASSWORD = os.getenv("STARROCKS_PASSWORD", "")
STARROCKS_DB = os.getenv("STARROCKS_DB", "retail_development")

def get_mysql_connection_string(db=None):
    database = db if db else STARROCKS_DB
    return f"mysql+mysqlconnector://{STARROCKS_USER}:{STARROCKS_PASSWORD}@{STARROCKS_HOST}:{STARROCKS_PORT}/{database}"

def get_auth():
    return (STARROCKS_USER, STARROCKS_PASSWORD)
