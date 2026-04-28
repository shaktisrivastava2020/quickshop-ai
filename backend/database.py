"""
QuickShop AI - Database Connection Module
Manages Cloud SQL PostgreSQL connection via Cloud SQL Python Connector.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from google.cloud.sql.connector import Connector, IPTypes
import pg8000

from config import get_settings

settings = get_settings()

# Singleton connector instance
_connector: Connector | None = None
_engine: Engine | None = None


def _get_connector() -> Connector:
    """Lazy-init the Cloud SQL Connector."""
    global _connector
    if _connector is None:
        _connector = Connector(ip_type=IPTypes.PUBLIC)
    return _connector


def _getconn():
    """Connection factory used by SQLAlchemy."""
    connector = _get_connector()
    conn = connector.connect(
        settings.db_instance_connection_name,
        "pg8000",
        user=settings.db_user,
        password=settings.db_password,
        db=settings.db_name,
    )
    return conn


def get_engine() -> Engine:
    """Get a SQLAlchemy engine - reused across requests."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            "postgresql+pg8000://",
            creator=_getconn,
            pool_size=5,
            max_overflow=2,
            pool_timeout=30,
            pool_recycle=1800,
        )
    return _engine


def execute_query(sql: str, params: dict | None = None) -> list[dict]:
    """
    Execute a read-only SQL query and return results as list of dicts.
    Used by the NL2SQL engine.
    """
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]


def get_table_schema() -> str:
    """
    Returns a human-readable schema description.
    Used to give Gemini context for NL2SQL generation.
    """
    schema = """
DATABASE SCHEMA - QuickShop AI E-commerce DB
=============================================

TABLE: customers
  - customer_id (INT, PK)
  - full_name (VARCHAR)
  - email (VARCHAR)
  - phone (VARCHAR)
  - city (VARCHAR)        -- e.g. 'Mumbai', 'Bangalore'
  - state (VARCHAR)       -- e.g. 'Maharashtra'
  - country (VARCHAR)     -- default 'India'
  - join_date (DATE)
  - customer_tier (VARCHAR) -- 'Standard', 'Premium', 'Gold'

TABLE: products
  - product_id (INT, PK)
  - product_name (VARCHAR)
  - category (VARCHAR)         -- 'Apparel','Electronics','Home','Beauty','Sports'
  - sub_category (VARCHAR)     -- e.g. 'Smartphones','T-Shirts'
  - brand (VARCHAR)            -- e.g. 'Nike','Boat','Mamaearth'
  - price (DECIMAL)
  - discount_percentage (INT)
  - size (VARCHAR)
  - color (VARCHAR)
  - description (TEXT)
  - rating (DECIMAL)
  - is_active (BOOLEAN)
  - created_date (DATE)

TABLE: inventory
  - inventory_id (INT, PK)
  - product_id (INT, FK -> products)
  - warehouse_location (VARCHAR) -- e.g. 'Mumbai-WH1','Delhi-WH2'
  - quantity_in_stock (INT)
  - reorder_level (INT)
  - last_restocked (DATE)

TABLE: orders
  - order_id (INT, PK)
  - customer_id (INT, FK -> customers)
  - product_id (INT, FK -> products)
  - quantity (INT)
  - order_amount (DECIMAL)
  - order_status (VARCHAR) -- 'Delivered','Shipped','Processing','Cancelled','Returned'
  - payment_method (VARCHAR) -- 'UPI','Credit Card','Debit Card','Cash on Delivery'
  - order_date (TIMESTAMP)
  - delivery_date (DATE)
  - shipping_address (TEXT)

RELATIONSHIPS:
  orders.customer_id -> customers.customer_id
  orders.product_id  -> products.product_id
  inventory.product_id -> products.product_id
"""
    return schema.strip()


def health_check() -> bool:
    """Quick DB connectivity test."""
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"DB health check failed: {e}")
        return False
