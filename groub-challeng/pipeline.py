import json
import argparse
from pathlib import Path
from describer import generate_description
from ingest_products import fetch_products

def load_products(input_path="data/raw/products.json"):
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_descriptions(products, output_dir="data/descriptions/"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    descriptions_by_category = {}

    for product in products:
        category = product["category"]
        product["generated_description"] = generate_description(product)

        # Keep only useful fields for HTML
        simplified = {
            "title": product["title"],
            "category": category,
            "brand": product.get("brand"),
            "price": product.get("price"),
            "rating": product.get("rating"),
            "availabilityStatus": product.get("availabilityStatus"),
            "thumbnail": product.get("thumbnail"),
            "generated_description": product["generated_description"]
        }

        descriptions_by_category.setdefault(category, []).append(simplified)

    for category, items in descriptions_by_category.items():
        file_path = Path(output_dir) / f"{category}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)
        print(f"[INFO] Saved {len(items)} items under '{category}'")

def main(category_filter=None):
    fetch_products()
    products = load_products()
    if category_filter:
        products = [p for p in products if p["category"].lower() == category_filter.lower()]
    save_descriptions(products)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", help="Specify category to generate descriptions for")
    args = parser.parse_args()

    main(category_filter=args.category)
