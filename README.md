# Python fundamentals WEEK 04
🛒 Shopping List CLI

Simple CLI app to manage a shopping list with saved product prices.

📁 Files overview
# shop.py
Entry point (CLI)
Parses commands (add, list, total, clear)
Calls logic functions
Saves data if operation succeeds
# storage.py
Handles JSON files
shopping.json → current shopping list
prices.json → saved product prices
# shopping.json
Stores active shopping list
[
  { "product_name": "Siers", "quantity": 3, "price": 3.49 }
]
# prices.json
Stores product names and prices. Needed for fast look up. 