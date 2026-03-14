class Product:
    """
    Represents an individual product within the inventory.
    This class serves as a data model for products, capturing essential
    details such as pricing, categorization, and availability. It is
    designed to be easily convertible for database operations.
    Attributes:
        name (str): The display name of the product.
        price (float): The unit price of the product.
        category (str): The grouping or department the product belongs to.
        stock_count (int): The current quantity available in inventory.
    """

    def __init__(self, name: str, price: float,
                 category: str, stock_count: int) -> None:
        """
        Initializes the product object
        Args:
            name (str): The name of the product.
            price (float): The price of the product.
            category (str): The category the product falls under.
            stock_count (int): Initial number of items in stock."""
        self.name = name
        self.price = price
        self.category = category
        self.stock_count = stock_count

    def to_dict(self) -> dict:
        """
        Converts the product instance into a dictionary format.
        This method is ideal for preparing data for NoSQL databases (like MongoDB)
        or for JSON API responses.
        Returns dict[str, Any]: A dictionary containing all product attributes.
        """
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
