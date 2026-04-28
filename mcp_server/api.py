import os
import requests

class EcommerceAPI:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("REAL_API_KEY")
        self.use_real_api = bool(self.api_key)

    def search_products(self, query: str, category: str = None):
        try:
            if self.use_real_api:
                print(f"Using real API for searching: {self.api_key}")
                pass # e.g., mapping to SerpAPI here

            if category and not query:
                url = f"https://dummyjson.com/products/category/{category}"
            else:
                url = f"https://dummyjson.com/products/search?q={query}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            return [
                {
                    "id": str(p["id"]),
                    "title": p.get("title"),
                    "description": p.get("description"),
                    "price": p.get("price"),
                    "category": p.get("category"),
                    "brand": p.get("brand"),
                    "rating": p.get("rating"),
                    "url": f"https://dummyjson.com/products/{p['id']}"
                }
                for p in data.get("products", [])
            ]
        except Exception as e:
            print(f"Error searching products: {e}")
            raise Exception(f"Failed to search products: {e}")

    def get_product_details(self, product_id: str):
        try:
            if self.use_real_api:
                pass
            
            response = requests.get(f"https://dummyjson.com/products/{product_id}")
            response.raise_for_status()
            p = response.json()
            return {
                "id": str(p["id"]),
                "title": p.get("title"),
                "description": p.get("description"),
                "price": p.get("price"),
                "category": p.get("category"),
                "brand": p.get("brand"),
                "rating": p.get("rating"),
                "reviews": p.get("reviews", []),
                "url": f"https://dummyjson.com/products/{p['id']}"
            }
        except Exception as e:
            raise Exception(f"Failed to get product details: {e}")

    def get_price_comparisons(self, product_id: str):
        try:
             product = self.get_product_details(product_id)
             base_price = product.get("price", 0)
             comps = [
                 {"store": "Mockzon", "price": base_price * 1.05, "inStock": True, "url": f"https://mockzon.com/{product_id}"},
                 {"store": "Walmock", "price": base_price * 0.98, "inStock": True, "url": f"https://walmock.com/{product_id}"},
                 {"store": "Targmock", "price": base_price * 1.02, "inStock": False, "url": f"https://targmock.com/{product_id}"}
             ]
             return sorted(comps, key=lambda x: x["price"])
        except Exception as e:
             raise Exception(f"Failed to compare prices: {e}")

ecommerce_api = EcommerceAPI()
