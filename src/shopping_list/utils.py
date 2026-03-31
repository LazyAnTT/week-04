def normalize_product_name(name: str) -> str:
    """Uppercase and strip spaces."""
    return name.strip().capitalize()


def normalize_price(price: str) -> float:
    """
    Validate and normalize price:
    - accepts comma or dot
    - ensures it's a float
    - ensures float is positive
    """
    price = price.strip().replace(",", ".").replace("-", "")

    try:
        value = float(price)
    except ValueError:
        raise ValueError("Cena nav derīgs skaitlis.")

    return value
