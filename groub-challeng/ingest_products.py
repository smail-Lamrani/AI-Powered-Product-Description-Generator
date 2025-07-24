import requests
import json
from pathlib import Path

def fetch_products(output_path="data/raw/products.json"):
    url = "https://dummyjson.com/products?limit=10"
    response = requests.get(url)
    response.raise_for_status()
    products = response.json()["products"]

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2)

    print(f"[INFO] Saved {len(products)} products to {output_path}")

if __name__ == "__main__":
    fetch_products()
