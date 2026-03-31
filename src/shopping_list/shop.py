import sys
import storage
import utils


def add_product(shopping_list, product_name=None, quantity=None, price=None):
    """Add a new product to the products list."""

    # --- PRODUCT NAME ---
    if product_name is None:
        product_name = input("Ievadiet preces nosaukumu: ")

    product_name = utils.normalize_product_name(product_name)

    # --- QUANTITY ---
    max_quantity = 99

    if quantity is None:
        while True:
            quantity_input = input(f"Ievadiet preču skaitu (no 1-{max_quantity}): ")

            try:
                quantity = int(quantity_input)
            except ValueError:
                print("Lūdzu ievadiet derīgu skaitli.")
                continue

            if 1 <= quantity <= max_quantity:
                break
            else:
                print(f"Skaitlim jābūt no 1 līdz {max_quantity}.")
    else:
        try:
            quantity = int(quantity)
        except ValueError:
            print("Kļūda: preču skaitam jābūt veselam skaitlim.")
            return False

        if not (1 <= quantity <= max_quantity):
            print(f"Kļūda: preču skaitam jābūt no 1 līdz {max_quantity}.")
            return False

    # --- PRICE ---
    if price is None:
        while True:
            price_input = input("Ievadiet preces cenu: ")

            try:
                price = utils.normalize_price(price_input)
                break
            except ValueError as e:
                print(f"Kļūda: {e}")
    else:
        try:
            price = utils.normalize_price(price)
        except ValueError as e:
            print(f"Kļūda: {e}")
            return False

    # --- SAVE ---
    shopping_list.append(
        {"product_name": product_name, "quantity": quantity, "price": price}
    )

    # --- CALCULATE TOTAL ---
    total = price * quantity

    # --- PRINT ---
    print(
        f"Pievienots: {product_name} × {quantity} — ({price:.2f} EUR/gab) = {total:.2f} EUR"
    )

    return True


def list_products(shopping_list):
    """Display all products."""
    if not shopping_list:
        print("Preču saraksts ir tukšs.")
        return

    print("\nPreču saraksts:")
    for i, product in enumerate(shopping_list, start=1):
        print(
            f"{i}. {product['product_name']} × {product['quantity']} — "
            f"{product['price']:.2f} EUR/gab — "
            f"{(product['price'] * product['quantity']):.2f} EUR"
        )


def total_price(shopping_list):
    """Sum of all shopping list products."""
    if not shopping_list:
        print("Preču saraksts ir tukšs.")
        return

    product_count = len(shopping_list)
    total_sum = 0.0
    total_units = 0

    for product in shopping_list:
        total_sum += product["price"] * product["quantity"]
        total_units += product["quantity"]

    print(
        f"Kopā: {total_sum:.2f} EUR "
        f"({total_units} {'vienība' if total_units == 1 else 'vienības'}, "
        f"{product_count} {'produkts' if product_count == 1 else 'produkti'})"
    )


def handle_clear(shopping_list):
    """Clear all shopping list data."""
    if not shopping_list:
        print("Preču saraksts jau ir tukšs.")
        return

    confirm = input("Vai tiešām dzēst VISU sarakstu? (y/n): ").strip().lower()

    if confirm == "y":
        storage.clear_shopping_list()
        shopping_list.clear()
        print("Preču saraksts ir notīrīts.")
    else:
        print("Darbība atcelta.")


COMMANDS = {
    "list": list_products,
    "total": total_price,
    "clear": handle_clear,
}


if __name__ == "__main__":
    shopping_list = storage.load_shopping_list()

    if len(sys.argv) < 2:
        print("Lietošana:")
        print("  python shop.py add")
        print("  python shop.py add <nosaukums> <daudzums> <cena>")
        print("  python shop.py list")
        print("  python shop.py total")
        print("  python shop.py clear")
        sys.exit()

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) == 2:
            success = add_product(shopping_list)
        elif len(sys.argv) == 5:
            success = add_product(shopping_list, sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Kļūda: nepareizs parametru skaits komandai 'add'.")
            print("Lietošana:")
            print("  python shop.py add")
            print("  python shop.py add <nosaukums> <daudzums> <cena>")
            sys.exit()

        if success:
            storage.save_shopping_list(shopping_list)

    elif command in COMMANDS:
        COMMANDS[command](shopping_list)

    else:
        print("Nezināma komanda.")
