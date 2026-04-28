import sqlite3
import os
from datetime import datetime, timedelta

def seed_database():
    db_path = os.path.join(os.path.dirname(__file__), 'shopping.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Clear existing cart to avoid too much clutter during seed
    cursor.execute("DELETE FROM cart")

    # Insert Sample Budgets
    budgets = [
        ('electronics', 2000.0, 450.0),
        ('groceries', 500.0, 120.50),
        ('general', 5000.0, 300.0),
        ('clothing', 300.0, 50.0),
        ('home-decoration', 800.0, 0.0)
    ]
    for b in budgets:
        cursor.execute(
            "INSERT INTO budgets (category, amount, spent) VALUES (?, ?, ?) ON CONFLICT(category) DO UPDATE SET amount = excluded.amount, spent = excluded.spent", 
            b
        )

    # Insert Sample Cart Items (Using common DummyJSON IDs)
    cart_items = [
        ('1', 'Essence Mascara Lash Princess', 9.99, 2),
        ('2', 'Eyeshadow Palette with Mirror', 19.99, 1),
        ('121', 'iPhone 5s', 149.99, 1),
        ('122', 'iPhone 6', 199.99, 1),
        ('125', 'Oppo A57', 249.99, 1)
    ]
    for item in cart_items:
        cursor.execute("INSERT INTO cart (productId, title, price, quantity) VALUES (?, ?, ?, ?)", item)

    # Insert Sample Orders with dynamic times
    time_a = (datetime.utcnow() - timedelta(days=2)).isoformat()
    time_b = (datetime.utcnow() - timedelta(minutes=180)).isoformat()
    time_c = (datetime.utcnow() - timedelta(days=5)).isoformat()
    
    orders = [
        ('ORD-99911', 'Shipped', time_a),
        ('ORD-10020', 'Processing', time_b),
        ('ORD-55555', 'Delivered', time_c),
        ('ORD-77777', 'Packed', time_b)
    ]
    
    for order in orders:
        # replace if exists based on ID
        cursor.execute("INSERT OR REPLACE INTO orders (id, status, updatedAt) VALUES (?, ?, ?)", order)

    conn.commit()
    conn.close()
    print("Successfully seeded the database with rich mock data! (Budgets, Cart Items, and Tracked Orders)")

if __name__ == "__main__":
    seed_database()
