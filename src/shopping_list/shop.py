import sys
import storage
import utils


def add_product(shopping_list):
    """Add a new product to the products list."""

    product_name = input("Ievadiet preces nosaukumu: ")
    product_name = utils.normalize_product_name(product_name)

    while True:
        price_input = input("Ievadiet preces cenu: ")

        try:
            price = utils.normalize_price(price_input)
            break  #  exit loop when valid
        except ValueError as e:
            print(f"Kļūda: {e}")

    shopping_list.append({"product_name": product_name, "price": price})

    print(f"Pievienots: {product_name} ({price} EUR)")


def list_products(shopping_list):
    """Display all products."""
    if not shopping_list:
        print("Preču saraksts ir tukšs.")
        return

    print("\nPreču saraksts:")
    for i, product in enumerate(shopping_list, start=1):
        print(f"{i}. {product['product_name']} - {product['price']} EUR")


def total_price(shopping_list):
    """Summ of all shopping list products"""
    if not shopping_list:
        print("Preču saraksts ir tukšs.")
        return

    productCount = len(product_list)
    total = 0.0

    for product in shopping_list:
        total += float(product["price"])

    print(
        f"Kopā: {total:.2f} EUR ({productCount} {'produkts' if productCount == 1 else 'produkti'})"
    )


if __name__ == "__main__":
    product_list = storage.load_shopping_list()

    if len(sys.argv) < 2:
        print("Lietošana:")
        print("  python shop.py list")
        print("  python shop.py add")
        print(" python shop.py total")
        sys.exit()

    command = sys.argv[1]

    if command == "list":
        list_products(product_list)

    elif command == "add":
        add_product(product_list)
        storage.save_shopping_list(product_list)
    elif command == "clear":
        confirm = input("Vai tiešām dzēst VISU sarakstu? (y/n): ")

        if confirm.lower() == "y":
            storage.clear_shopping_list()
            print("Saraksts ir notīrīts.")
        else:
            print("Darbība atcelta.")
    elif command == "total":
        total_price(product_list)

    else:
        print("Nezināma komanda.")
