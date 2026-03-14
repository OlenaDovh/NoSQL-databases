from pymongo.errors import PyMongoError
from typing import Literal, Optional, Any
from config.db_connection import products_col
from models.product import Product

import logging

logger = logging.getLogger(__name__)


def create_product(name: str, price: float, category: str, stock_count: int) -> Optional[dict[str, str]]:
    """
    Creates a new product in the database if it does not already exist.
    Args:
        name (str): The name of the product.
        price (float): The unit price of the product.
        category (str): The product category.
        stock_count (int): Initial quantity in stock.

    Returns Optional[dict[str, str]]: A dictionary with 'inserted_id' if successful,
                                      None if the product already exists.
    Raises PyMongoError: If a database error occurs during insertion.
    """
    try:
        if products_col.find_one({"name": name}):
            logger.warning(f"Product '{name}' already exists")
            return None
        product = Product(name, price, category, stock_count)
        result = products_col.insert_one(product.to_dict())
        logger.info(f"Товар '{name}' успішно створено, наявна кількість: {get_product_count_in_stock(name)}")
        return {"inserted_id": str(result.inserted_id)}
    except PyMongoError as e:
        logger.error(f"Виникла помилка при створенні товару '{name}': {e}")
        raise


def get_product_count_in_stock(product_name: str) -> int:
    """
    Retrieves the current stock quantity for a specific product.
    Args product_name (str): The name of the product to check.
    Returns int: The quantity available in stock. Returns 0 if product is not found.
    """
    product = products_col.find_one({"name": product_name})

    if not product:
        logger.warning(f"Товар '{product_name}' не знайдено")
        return 0

    return product["stock_count"]


def update_prods_in_stock(product_name: str, count: int,
                          action: Literal["add", "remove"] = "add") -> None:
    """
    Updates the stock count for a given product by adding or removing items.
    Args:
        product_name (str): The name of the product to update.
        count (int): The quantity to change by.
        action (Literal["add", "remove"]): The direction of the stock update.
    Raises:
        ValueError: If the product is not found or if removal exceeds available stock.
        Exception: For general database or logic errors.
    """
    try:
        product = products_col.find_one({"name": product_name})

        if not product:
            raise ValueError(f"Product '{product_name}' not found")

        current_count = product["stock_count"]

        if action == "remove" and current_count < count:
            raise ValueError(
                f"Cannot remove {count} items of '{product_name}'. Available: {current_count}"
            )

        change_count = count if action == "add" else -count

        products_col.update_one(
            {"name": product_name},
            {"$inc": {"stock_count": change_count}}
        )

        new_count = current_count + change_count

        logger.info(
            f"Запаси товару '{product_name}' оновлено. Було:{change_count}, стало: {new_count}"
        )

    except Exception as e:
        logger.error(f"Помилка оновлення запасів товару '{product_name}': {e}")
        raise


def delete_unavailable_products() -> None:
    """Removes all products from the database that have a stock count of zero or less"""
    try:
        result = products_col.delete_many({
            "stock_count": {"$lte": 0}
        })
        logger.info(f"Видалено {result.deleted_count} найменувань відсутніх товарів")

    except Exception as e:
        logger.error(f"Помилка видалення найменувань: {e}")
        raise


def get_product_price(product_name: str) -> float:
    """
    Retrieves the price of a specific product.
    Args product_name (str): The name of the product.
    Returns float: The unit price of the product.
    Raises ValueError: If the product is not found.
    """
    try:
        product = products_col.find_one({"name": product_name})

        if not product:
            raise ValueError(f"Товар '{product_name}' не знайдено")
        return product["price"]

    except Exception as e:
        logger.error(f"Помилка отримання ціни для '{product_name}': {e}")
        raise


def get_products_by_category(category: str) -> list[dict[str, Any]]:
    """
    Retrieves all products belonging to a specific category, sorted by price.
    Args category (str): The category name to filter by.
    Returns list[dict[str, Any]]: A list of product documents.
    Raises ValueError: If no products are found in the specified category.
    """
    try:
        result = list(products_col.find(
            {"category": category},
            {"_id": 0}).sort("price", 1))
        if category not in result:
            raise ValueError(f"Категорію '{category}' не знайдено")
        logger.info(f"Категорія '{category}': знайдено {len(result)} товарів.")
        return result
    except PyMongoError as e:
        logger.error(f"Помилка пошуку категорії '{category}': {e}")
        raise


def get_available_categories() -> list[str]:
    """
    Retrieves a list of all unique categories currently in the database.
    Returns list[str]: A list of category names. Returns an empty list if none exist.
    """
    try:
        categories = products_col.distinct("category")

        if not categories:
            logger.info("Наявних категорій не знайдено")
            return []

        return categories

    except Exception as e:
        logger.error(f"Помилка при отриманні списку категорій: {e}")
        raise
