import random
from datetime import datetime


def generate_order_num() -> int:
    """Function to generate random order number"""
    timestamp_part = int(datetime.now().timestamp())
    random_part = random.randint(1000, 9999)

    return int(f"{timestamp_part}{random_part}")
