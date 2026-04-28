"""
QuickShop AI - Fake Data Generator
Generates realistic e-commerce data for demo purposes.
Output: SQL INSERT statements written to data/seed_data.sql
"""

from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker('en_IN')  # Indian locale for realistic Indian customer data
Faker.seed(42)
random.seed(42)

# Output file
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'seed_data.sql')

# ============================================
# Reference data
# ============================================
CATEGORIES = {
    'Apparel': ['T-Shirts', 'Jeans', 'Dresses', 'Jackets', 'Shoes'],
    'Electronics': ['Smartphones', 'Laptops', 'Headphones', 'Smart Watches', 'Tablets'],
    'Home': ['Bedsheets', 'Curtains', 'Cookware', 'Decor', 'Storage'],
    'Beauty': ['Skincare', 'Haircare', 'Makeup', 'Fragrances'],
    'Sports': ['Yoga Mats', 'Dumbbells', 'Running Shoes', 'Cricket Gear']
}

BRANDS = ['Nykaa', 'Boat', 'Fastrack', 'Mamaearth', 'Wildcraft',
          'HRX', 'Roadster', 'Mivi', 'Lakme', 'Levis', 'Puma', 'Adidas']

COLORS = ['Black', 'White', 'Blue', 'Red', 'Green', 'Grey', 'Beige', 'Navy', 'Yellow']
SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'Free Size']
WAREHOUSES = ['Mumbai-WH1', 'Delhi-WH2', 'Bangalore-WH3', 'Chennai-WH4', 'Kolkata-WH5']
ORDER_STATUSES = ['Delivered', 'Delivered', 'Delivered', 'Shipped', 'Processing', 'Cancelled', 'Returned']
PAYMENT_METHODS = ['UPI', 'Credit Card', 'Debit Card', 'Cash on Delivery', 'Net Banking', 'Wallet']
TIERS = ['Standard', 'Standard', 'Standard', 'Premium', 'Premium', 'Gold']
INDIAN_CITIES = [
    ('Mumbai', 'Maharashtra'), ('Delhi', 'Delhi'), ('Bangalore', 'Karnataka'),
    ('Chennai', 'Tamil Nadu'), ('Kolkata', 'West Bengal'), ('Hyderabad', 'Telangana'),
    ('Pune', 'Maharashtra'), ('Ahmedabad', 'Gujarat'), ('Jaipur', 'Rajasthan'),
    ('Lucknow', 'Uttar Pradesh'), ('Bengaluru', 'Karnataka'), ('Chandigarh', 'Punjab')
]

# ============================================
# Generation functions
# ============================================
def gen_customers(n=200):
    rows = []
    for i in range(1, n+1):
        name = fake.name()
        email = f"{name.lower().replace(' ', '.').replace('.', '')[:15]}{i}@example.com"
        phone = f"+91{fake.msisdn()[3:]}"
        city, state = random.choice(INDIAN_CITIES)
        join_date = fake.date_between(start_date='-2y', end_date='today')
        tier = random.choice(TIERS)
        rows.append(f"('{name.replace(chr(39), chr(39)*2)}', '{email}', '{phone}', '{city}', '{state}', 'India', '{join_date}', '{tier}')")
    return rows

def gen_products(n=100):
    rows = []
    for i in range(1, n+1):
        category = random.choice(list(CATEGORIES.keys()))
        sub = random.choice(CATEGORIES[category])
        brand = random.choice(BRANDS)
        name = f"{brand} {sub} {fake.word().capitalize()}"
        price = round(random.uniform(199, 9999), 2)
        discount = random.choice([0, 0, 0, 10, 15, 20, 25, 30, 40, 50])
        size = random.choice(SIZES) if category in ['Apparel', 'Sports'] else 'Free Size'
        color = random.choice(COLORS)
        desc = fake.sentence(nb_words=10).replace("'", "''")
        rating = round(random.uniform(3.0, 5.0), 1)
        is_active = random.choice([True, True, True, True, False])
        rows.append(f"('{name.replace(chr(39), chr(39)*2)}', '{category}', '{sub}', '{brand}', {price}, {discount}, '{size}', '{color}', '{desc}', {rating}, {is_active})")
    return rows

def gen_inventory(n_products=100):
    rows = []
    for product_id in range(1, n_products+1):
        # Each product is in 1-3 warehouses
        warehouses = random.sample(WAREHOUSES, k=random.randint(1, 3))
        for wh in warehouses:
            qty = random.randint(0, 500)
            reorder = random.choice([10, 20, 50])
            last_restock = fake.date_between(start_date='-90d', end_date='today')
            rows.append(f"({product_id}, '{wh}', {qty}, {reorder}, '{last_restock}')")
    return rows

def gen_orders(n=1000, n_customers=200, n_products=100):
    rows = []
    for i in range(1, n+1):
        cust_id = random.randint(1, n_customers)
        prod_id = random.randint(1, n_products)
        qty = random.randint(1, 5)
        amount = round(random.uniform(199, 25000), 2)
        status = random.choice(ORDER_STATUSES)
        payment = random.choice(PAYMENT_METHODS)
        order_date = fake.date_time_between(start_date='-180d', end_date='now')
        delivery = (order_date + timedelta(days=random.randint(2, 10))).date() if status in ['Delivered', 'Shipped'] else None
        delivery_str = f"'{delivery}'" if delivery else 'NULL'
        addr = fake.address().replace("\n", ", ").replace("'", "''")
        rows.append(f"({cust_id}, {prod_id}, {qty}, {amount}, '{status}', '{payment}', '{order_date}', {delivery_str}, '{addr}')")
    return rows

# ============================================
# Write to SQL file
# ============================================
def write_sql():
    with open(OUTPUT_FILE, 'w') as f:
        f.write("-- QuickShop AI - Seed Data\n")
        f.write("-- Auto-generated. Do not edit manually.\n\n")
        
        # Customers
        f.write("-- Customers\n")
        f.write("INSERT INTO customers (full_name, email, phone, city, state, country, join_date, customer_tier) VALUES\n")
        f.write(",\n".join(gen_customers()))
        f.write(";\n\n")
        
        # Products
        f.write("-- Products\n")
        f.write("INSERT INTO products (product_name, category, sub_category, brand, price, discount_percentage, size, color, description, rating, is_active) VALUES\n")
        f.write(",\n".join(gen_products()))
        f.write(";\n\n")
        
        # Inventory
        f.write("-- Inventory\n")
        f.write("INSERT INTO inventory (product_id, warehouse_location, quantity_in_stock, reorder_level, last_restocked) VALUES\n")
        f.write(",\n".join(gen_inventory()))
        f.write(";\n\n")
        
        # Orders
        f.write("-- Orders\n")
        f.write("INSERT INTO orders (customer_id, product_id, quantity, order_amount, order_status, payment_method, order_date, delivery_date, shipping_address) VALUES\n")
        f.write(",\n".join(gen_orders()))
        f.write(";\n\n")
    
    print(f"✓ Seed data written to {OUTPUT_FILE}")

if __name__ == '__main__':
    write_sql()
