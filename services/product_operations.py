from pymongo.errors import PyMongoError
from typing import Literal
from config.db_connection import products_col
from models.product import Product

import logging

logger = logging.getLogger(__name__)


def create_product(name: str, price: float, category: str, stock_count: int) -> dict | None:
    """Creates new product and returns it id"""
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


def get_product_count_in_stock(product_name: str) -> int | None:
    """Returns count of products available in stock"""
    product = products_col.find_one({"name": product_name})

    if not product:
        logger.warning(f"Товар '{product_name}' не знайдено")
        return 0

    return product["stock_count"]


def update_prods_in_stock(product_name: str, count: int,
                          action: Literal["add", "remove"] = "add") -> None:
    """Updates product stock count"""
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
    """Deletes all unavailable products"""
    try:
        result = products_col.delete_many({
            "stock_count": {"$lte": 0}
        })
        logger.info(f"Видалено {result.deleted_count} найменувань відсутніх товарів")

    except Exception as e:
        logger.error(f"Помилка видалення найменувань: {e}")
        raise


def get_product_price(product_name: str) -> float:
    """Returns price of product"""
    try:
        product = products_col.find_one({"name": product_name})

        if not product:
            raise ValueError(f"Товар '{product_name}' не знайдено")
        return product["price"]

    except Exception as e:
        logger.error(f"Помилка отримання ціни для '{product_name}': {e}")
        raise


def get_products_by_category(category: str) -> list:
    """Returns list of products. Returns empty list if none found."""
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


def get_available_categories() -> list:
    """Returns list of available categories"""
    try:
        categories = products_col.distinct("category")

        if not categories:
            logger.info("Наявних категорій не знайдено")
            return []

        return categories

    except Exception as e:
        logger.error(f"Помилка при отриманні списку категорій: {e}")
        raise
