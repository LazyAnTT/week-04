import sys
import storage
import utils
import constants


def validate_product_name(product_name):
    """Validate and normalize product name."""
    if not isinstance(product_name, str) or not product_name.strip():
        print("Kļūda: preces nosaukums nav derīgs.")
        return None

    return utils.normalize_product_name(product_name)


def validate_quantity(quantity):
    """Validate quantity and convert to int."""
    max_quantity = constants.max_quantity

    try:
        quantity = int(quantity)
    except ValueError:
        print("Kļūda: preču skaitam jābūt veselam skaitlim.")
        return None

    if not (1 <= quantity <= max_quantity):
        print(f"Kļūda: preču skaitam jābūt no 1 līdz {max_quantity}.")
        return None

    return quantity


def update_product_price(product_name, price):
    """Update prices.json and notify if price changed."""
    prices = storage.load_prices()
    old_price = prices.get(product_name)

    prices[product_name] = price
    storage.save_prices(prices)

    if old_price is None or old_price != price:
        print(f"✓ Cena atjaunināta: {product_name} → {price:.2f} EUR")


def save_product(shopping_list, product_name, quantity, price):
    """Save product to shopping list and print result."""
    shopping_list.append(
        {"product_name": product_name, "quantity": quantity, "price": price}
    )

    total = price * quantity

    print(
        f"✓ Pievienots: {product_name} × {quantity} — ({price:.2f} EUR/gab) = {total:.2f} EUR"
    )


def add_product_interactive(shopping_list):
    """Add product step by step with prompts."""

    # --- PRODUCT NAME ---
    product_name = input("Ievadiet preces nosaukumu: ")
    product_name = validate_product_name(product_name)
    if product_name is None:
        return False

    # --- QUANTITY ---
    while True:
        quantity_input = input(
            f"Ievadiet preču skaitu (no 1-{constants.max_quantity}): "
        )
        quantity = validate_quantity(quantity_input)
        if quantity is not None:
            break

    # --- PRICE ---
    while True:
        price_input = input("Ievadiet preces cenu: ")
        try:
            price = utils.normalize_price(price_input)
            break
        except ValueError as e:
            print(f"Kļūda: {e}")

    update_product_price(product_name, price)
    save_product(shopping_list, product_name, quantity, price)
    return True


def add_product_with_quantity(shopping_list, product_name, quantity):
    """Add product with CLI name and quantity. Price is suggested or prompted."""

    # --- PRODUCT NAME ---
    product_name = validate_product_name(product_name)
    if product_name is None:
        return False

    # --- QUANTITY ---
    quantity = validate_quantity(quantity)
    if quantity is None:
        return False

    # --- PRICE ---
    suggested_price = storage.get_price(product_name)

    if suggested_price is not None:
        print(f"Atrasta cena: {suggested_price:.2f} EUR/gab")

        while True:
            use_existing = input("Vai izmantot šo cenu? (y/n): ").strip().lower()

            if use_existing == "y":
                price = suggested_price
                break
            elif use_existing == "n":
                while True:
                    price_input = input("Ievadiet jauno cenu: ")
                    try:
                        price = utils.normalize_price(price_input)
                        break
                    except ValueError as e:
                        print(f"Kļūda: {e}")
                break
            else:
                print("Lūdzu ievadiet 'y' vai 'n'.")
    else:
        while True:
            price_input = input("Ievadiet preces cenu: ")
            try:
                price = utils.normalize_price(price_input)
                break
            except ValueError as e:
                print(f"Kļūda: {e}")

    update_product_price(product_name, price)
    save_product(shopping_list, product_name, quantity, price)
    return True


def add_product_full(shopping_list, product_name, quantity, price):
    """Add product with CLI name, quantity and price."""

    # --- PRODUCT NAME ---
    product_name = validate_product_name(product_name)
    if product_name is None:
        return False

    # --- QUANTITY ---
    quantity = validate_quantity(quantity)
    if quantity is None:
        return False

    # --- PRICE ---
    try:
        price = utils.normalize_price(price)
    except ValueError as e:
        print(f"Kļūda: {e}")
        return False

    update_product_price(product_name, price)
    save_product(shopping_list, product_name, quantity, price)
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
        print("  python shop.py add <nosaukums> <daudzums>")
        print("  python shop.py add <nosaukums> <daudzums> <cena>")
        print("  python shop.py list")
        print("  python shop.py total")
        print("  python shop.py clear")
        sys.exit()

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) == 2:
            success = add_product_interactive(shopping_list)
        elif len(sys.argv) == 4:
            success = add_product_with_quantity(shopping_list, sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            success = add_product_full(
                shopping_list, sys.argv[2], sys.argv[3], sys.argv[4]
            )
        else:
            print("Kļūda: nepareizs parametru skaits komandai 'add'.")
            print("Lietošana:")
            print("  python shop.py add")
            print("  python shop.py add <nosaukums> <daudzums>")
            print("  python shop.py add <nosaukums> <daudzums> <cena>")
            sys.exit()

        if success:
            storage.save_shopping_list(shopping_list)

    elif command in COMMANDS:
        COMMANDS[command](shopping_list)

    else:
        print("Nezināma komanda.")
