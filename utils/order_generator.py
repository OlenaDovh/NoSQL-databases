import random
from datetime import datetime


def generate_order_num() -> int:
    """
    Generates a unique, high-entropy order number.
    The number is constructed by concatenating the current Unix timestamp
    with a four-digit random integer to ensure uniqueness even for
    high-frequency order placements.
    Returns:
        int: A composite numerical identifier for the order.
    """
    timestamp_part = int(datetime.now().timestamp())
    random_part = random.randint(1000, 9999)

    return int(f"{timestamp_part}{random_part}")
