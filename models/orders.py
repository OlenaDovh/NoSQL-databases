from datetime import datetime

import logging
from typing import Any

logger = logging.getLogger(__name__)


class Order:
    """
    Represents a customer order in the system.
    This class encapsulates all details regarding a specific purchase,
    including product list, pricing, and timestamp. It provides utility
    methods for data conversion and string representation.
    Attributes:
        order_number (int): Unique identifier for the order.
        user (str): Username or name of the customer.
        products (List[Any]): A list of products included in the order.
        total_price (float): The total monetary value of the order.
        date (datetime): The timestamp when the order was created.
    """

    def __init__(self, order_number: int, user: str,
                 products: list[Any], total_price: float) -> None:
        """
        Initializes a new Order instance.
        Args:
            order_number (int): The unique ID of the order.
            user (str): The customer associated with the order.
            products (List[Any]): List of items (usually dicts or IDs).
            total_price (float): Total cost of the transaction.
        """
        self.order_number = order_number
        self.user = user
        self.products = products
        self.total_price = total_price
        self.date = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        """
        Converts the order instance into a dictionary format.
        This is particularly useful for JSON serialization or
        storing data in NoSQL databases like MongoDB.
        Returns dict[str, Any]: A dictionary containing all order details.
        """
        return {
            "order_number": self.order_number,
            "user": self.user,
            "products": self.products,
            "total_price": self.total_price,
            "date": self.date
        }

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the order.
        """
        date_str = self.date.strftime("%d.%m.%Y %H:%M")
        return (f"Замовлення №{self.order_number} від {date_str}\n"
                f"Клієнт: {self.user}\n"
                f"Сума: {self.total_price} грн\n"
                f"Товари: {self.products}")
