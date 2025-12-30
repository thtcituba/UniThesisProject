import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    conn_str = os.getenv("DB_CONN_STR")  # <<< BU İSİM ŞART
    if not conn_str:
        raise RuntimeError("DB_CONN_STR not found in .env")
    return pyodbc.connect(conn_str)

print("USING DB_CONN_STR:", os.getenv("DB_CONN_STR"))
