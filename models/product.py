class Product:
    """Represents an individual product"""

    def __init__(self, name: str, price: float, category: str, stock_count: int) -> None:
        """Initializes the product object"""
        self.name = name
        self.price = price
        self.category = category
        self.stock_count = stock_count

    def to_dict(self) -> dict:
        """Converts the product to a dictionary"""
        return {
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "stock_count": self.stock_count
        }

    def __str__(self) -> str:
        """Returns a string representation of the product"""
        return (f"Product name: {self.name},\n"
                f"price: {self.price},\n"
                f"category: {self.category},\n"
                f"stock: {self.stock_count}")
