import os
import json


def load_shopping_list(shopping_file="shopping.json"):
    """Load products from the JSON file. If the file does not exist, is empty, or is invalid, return an empty list."""
    if not os.path.exists(shopping_file):
        return []

    with open(shopping_file, "r", encoding="utf-8") as products:
        content = products.read().strip()

        if not content:
            return []

        return json.loads(content)


def save_shopping_list(shopping_list, shopping_file="shopping.json"):
    """Save the shopping list to the JSON file."""
    with open(shopping_file, "w", encoding="utf-8") as file:
        json.dump(shopping_list, file, ensure_ascii=False, indent=2)


def clear_shopping_list(shopping_file="shopping.json"):
    """Clear all data in the shopping list (reset to empty list)."""
    with open(shopping_file, "w", encoding="utf-8") as file:
        json.dump([], file, ensure_ascii=False, indent=2)


def load_prices(prices_file="prices.json"):
    if not os.path.exists(prices_file):
        return {}

    with open(prices_file, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}


def save_prices(prices, prices_file="prices.json"):
    with open(prices_file, "w", encoding="utf-8") as f:
        json.dump(prices, f, ensure_ascii=False, indent=2)


def get_price(product_name):
    """Get stored price for a product, or None if not found."""
    prices = load_prices()
    return prices.get(product_name)
