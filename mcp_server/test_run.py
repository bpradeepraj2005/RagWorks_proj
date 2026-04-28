from main import search_products, get_product_reviews, set_budget, add_to_cart, check_budget, track_delivery

print("===== SHOPPING ASSISTANT MCP TESTER =====")

print("\n[1] Testing Search Products ('laptop')...")
print(search_products("laptop", None))

print("\n[2] Testing Budget Set ('laptops' -> $1500)...")
print(set_budget("laptops", 1500.0))

print("\n[3] Adding a Laptop to Cart (Dummy Product ID: 7)...")
print(add_to_cart("7", 1))

print("\n[4] Checking Budget Status...")
print(check_budget("laptops"))

print("\n[5] Getting Product Reviews (Dummy Product ID: 7)...")
print(get_product_reviews("7"))

print("\n[6] Tracking a Delivery (Order: 'ORD-54321')...")
print(track_delivery("ORD-54321"))

print("\n=========================================")
