from datetime import datetime

import logging

logger = logging.getLogger(__name__)


class Order:
    """Represents an order"""

    def __init__(self, order_number: int, user: str, products: list, total_price: float) -> None:
        """Initialize an order"""
        self.order_number = order_number
        self.user = user
        self.products = products
        self.total_price = total_price
        self.date = datetime.now()

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the order"""
        return {
            "order_number": self.order_number,
            "user": self.user,
            "products": self.products,
            "total_price": self.total_price,
            "date": self.date
        }

    def __str__(self) -> str:
        date_str = self.date.strftime("%d.%m.%Y %H:%M")
        return (f"Замовлення №{self.order_number} від {date_str}\n"
                f"Клієнт: {self.user}\n"
                f"Сума: {self.total_price} грн\n"
                f"Товари: {self.products}")