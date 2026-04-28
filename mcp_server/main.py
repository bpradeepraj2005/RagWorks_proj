from mcp.server.fastmcp import FastMCP
from api import ecommerce_api
from database import get_db
import json
from datetime import datetime, timedelta
from typing import Optional

mcp = FastMCP("shopping-assistant-mcp")

@mcp.tool()
def search_products(query: str, category: Optional[str] = None) -> str:
    """Search for products across e-commerce platforms.
    
    Args:
        query: Search query (e.g., 'smartphone', 'laptop')
        category: Optional category to filter by
    """
    try:
        products = ecommerce_api.search_products(query, category)
        return json.dumps(products, indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def compare_prices(product_id: str) -> str:
    """Compare prices for a specific product ID across different stores.
    
    Args:
        product_id: The ID of the product to compare (retrieved from search_products)
    """
    try:
        comps = ecommerce_api.get_price_comparisons(product_id)
        return json.dumps(comps, indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_product_reviews(product_id: str) -> str:
    """Get reviews and sentiment analysis for a specific product.
    
    Args:
        product_id: The ID of the product
    """
    try:
        product = ecommerce_api.get_product_details(product_id)
        reviews = product.get("reviews", [])
        rating = product.get("rating", 0)
        
        sentiment = "Neutral"
        if rating > 4: sentiment = "Highly Positive"
        elif rating > 3: sentiment = "Positive"
        elif rating < 2.5: sentiment = "Negative"
        
        return json.dumps({
            "rating": rating,
            "sentimentSummary": sentiment,
            "reviewCount": len(reviews),
            "topReviews": reviews[:3]
        }, indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def set_budget(category: str, amount: float) -> str:
    """Set a budget for a given category (or 'general').
    
    Args:
        category: Category for the budget (e.g., 'electronics', 'general')
        amount: The budget amount limit
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO budgets (category, amount, spent) 
                VALUES (?, ?, 0)
                ON CONFLICT(category) DO UPDATE SET amount = excluded.amount
            """, (category, amount))
            conn.commit()
        return f"Budget for {category} set to ${amount}."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def check_budget(category: Optional[str] = None) -> str:
    """Check all budgets or a specific category budget.
    
    Args:
        category: Optional category to check. If omitted, checks all.
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            if category:
                cursor.execute("SELECT * FROM budgets WHERE category = ?", (category,))
                res = cursor.fetchone()
                if not res:
                    return f"No budget found for {category}."
                return json.dumps(dict(res), indent=2)
            else:
                cursor.execute("SELECT * FROM budgets")
                rows = cursor.fetchall()
                return json.dumps([dict(row) for row in rows], indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def add_to_cart(product_id: str, quantity: int = 1) -> str:
    """Add a product to your cart, which subtracts from its category budget if tracked.
    
    Args:
        product_id: ID of the product
        quantity: Number of items
    """
    try:
        product = ecommerce_api.get_product_details(product_id)
        total_cost = product.get("price", 0) * quantity
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cart (productId, title, price, quantity) VALUES (?, ?, ?, ?)",
                (product['id'], product['title'], product['price'], quantity)
            )
            
            cursor.execute("SELECT * FROM budgets WHERE category = ?", (product['category'],))
            cat_budget = cursor.fetchone()
            
            cursor.execute("SELECT * FROM budgets WHERE category = 'general'")
            gen_budget = cursor.fetchone()
            
            warning = ""
            if cat_budget:
                cursor.execute("UPDATE budgets SET spent = spent + ? WHERE category = ?", (total_cost, product['category']))
                if cat_budget['spent'] + total_cost > cat_budget['amount']:
                    warning = f"\\nWARNING: You have exceeded your {product['category']} budget!"
            elif gen_budget:
                cursor.execute("UPDATE budgets SET spent = spent + ? WHERE category = 'general'", (total_cost,))
                if gen_budget['spent'] + total_cost > gen_budget['amount']:
                    warning = f"\\nWARNING: You have exceeded your general budget!"
            
            conn.commit()
            
        return f"Added {quantity}x {product['title']} to cart. Total cost: ${total_cost:.2f}.{warning}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_recommendations(category: str, max_price: Optional[float] = None) -> str:
    """Get personalized product recommendations based on a category and budget.
    
    Args:
        category: Category of product (e.g., 'smartphones')
        max_price: Maximum price for the recommendation
    """
    try:
        products = ecommerce_api.search_products(query="", category=category)
        if max_price is not None:
            products = [p for p in products if p.get("price", float('inf')) <= max_price]
            
        products.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return json.dumps(products[:5], indent=2)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def track_delivery(order_id: str) -> str:
    """Track the real-time status of a delivery/order.
    
    Args:
        order_id: Order ID tracking number
    """
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = cursor.fetchone()
            
            statuses = ["Processing", "Packed", "Shipped", "Out for Delivery", "Delivered"]
            status = "Processing"
            
            if not order:
                num = ord(order_id[0]) + len(order_id) if len(order_id) > 0 else 0
                status = statuses[num % len(statuses)]
                cursor.execute("INSERT INTO orders (id, status) VALUES (?, ?)", (order_id, status))
                conn.commit()
                last_update = datetime.utcnow().isoformat()
            else:
                status = order["status"]
                last_update = order["updatedAt"]
                
            est_del = (datetime.utcnow() + timedelta(days=3)).strftime('%Y-%m-%d')
            
            details = {
                "orderId": order_id,
                "status": status,
                "courier": "MockEx",
                "estimatedDelivery": est_del,
                "lastUpdate": last_update
            }
            return json.dumps(details, indent=2)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()
