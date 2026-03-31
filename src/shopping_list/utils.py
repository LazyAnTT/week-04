def normalize_product_name(name: str) -> str:
    """Uppercase and strip spaces."""
    return name.strip().capitalize()


def normalize_price(price: str) -> str:
    """
    Validate and normalize price:
    - accepts comma or dot
    - ensures it's a float
    - formats to 2 decimals
    - always uses dot
    """
    price = price.strip().replace(",", ".")

    try:
        value = float(price)
    except ValueError:
        raise ValueError("Cena nav derīgs skaitlis.")

    return f"{value:.2f}"
