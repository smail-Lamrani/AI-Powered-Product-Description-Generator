import cohere
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def generate_description(product):
    title = product["title"]
    category = product["category"]
    price = product["price"]
    rating = product["rating"]
    brand = product.get("brand", "Unknown brand")
    stock = product.get("stock", "N/A")
    warranty = product.get("warrantyInformation", "N/A")
    availability = product.get("availabilityStatus", "Unknown")

    prompt = (
        f"Write a friendly and different from previous short product description for a {category} item named '{title}', "
        f"by {brand}, priced at ${price}, rated {rating} stars, currently {availability}. "
        f"It has {stock} in stock and comes with a warranty of '{warranty}' and each time you recive this prompt be creative."
    )

    response = co.generate(model="command-r-plus", prompt=prompt, max_tokens=100)
    return response.generations[0].text.strip()
