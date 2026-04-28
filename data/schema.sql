-- QuickShop AI Database Schema
-- E-commerce data model for RAG + NL2SQL chatbot

-- Drop existing tables (clean slate for re-runs)
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ============================================
-- CUSTOMERS table
-- ============================================
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'India',
    join_date DATE DEFAULT CURRENT_DATE,
    customer_tier VARCHAR(20) DEFAULT 'Standard'
);

-- ============================================
-- PRODUCTS table
-- ============================================
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50),
    brand VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    discount_percentage INT DEFAULT 0,
    size VARCHAR(20),
    color VARCHAR(30),
    description TEXT,
    rating DECIMAL(2,1) DEFAULT 0.0,
    is_active BOOLEAN DEFAULT TRUE,
    created_date DATE DEFAULT CURRENT_DATE
);

-- ============================================
-- INVENTORY table
-- ============================================
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id) ON DELETE CASCADE,
    warehouse_location VARCHAR(50) NOT NULL,
    quantity_in_stock INT NOT NULL DEFAULT 0,
    reorder_level INT DEFAULT 10,
    last_restocked DATE
);

-- ============================================
-- ORDERS table
-- ============================================
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE SET NULL,
    product_id INT REFERENCES products(product_id) ON DELETE SET NULL,
    quantity INT NOT NULL,
    order_amount DECIMAL(10,2) NOT NULL,
    order_status VARCHAR(30) DEFAULT 'Pending',
    payment_method VARCHAR(30),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivery_date DATE,
    shipping_address TEXT
);

-- ============================================
-- INDEXES for query performance
-- ============================================
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_product ON orders(product_id);
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_inventory_product ON inventory(product_id);

-- Done!
