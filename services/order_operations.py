from datetime import datetime, timedelta
from typing import Any

from pymongo.results import InsertOneResult

from config.db_connection import orders_col
from pymongo.errors import PyMongoError
from models.orders import Order
import logging

logger = logging.getLogger(__name__)


def create_order(order: Order) -> InsertOneResult:
    """
    Inserts a new order document into the MongoDB collection.
    Args order (Order): An instance of the Order model.
    Returns InsertOneResult: The result object from MongoDB containing the inserted ID.
    Raises PyMongoError: If the database operation fails.
    """
    try:
        result = orders_col.insert_one(order.to_dict())
        logger.info(f"Order created | id={result.inserted_id}")
        return result
    except PyMongoError as e:
        logger.error(f"Database error while creating order: {e}")
        raise


def all_orders_for_last_period(period: int) -> list[dict[str, Any]]:
    """
    Retrieves all orders placed within a specified number of days.
    The method filters documents by date and formats the datetime objects
    into readable strings for reporting.
    Args period (int): Number of days to look back from the current time.
    Returns: list[dict[str, Any]]: A list of order documents without the MongoDB '_id'.
    """
    try:
        date_limit = datetime.now() - timedelta(days=period)

        orders = list(orders_col.find(
            {"date": {"$gte": date_limit}},
            {"_id": 0}
        ))

        for order in orders:
            if "date" in order and isinstance(order["date"], datetime):
                order["date"] = order["date"].strftime("%d-%m-%Y")
        logger.info(f"Оформлено {len(orders)} замовлень за останні {period} днів")
        return orders
    except Exception as e:
        logger.error(f"Помилка формування звіту: {e}")
        raise


def get_sold_products_count(period: int) -> list[dict[str, Any]]:
    """"
    Calculates the total quantity sold for each product within a given period.
    Uses an aggregation pipeline to unwind the products array and group
    by product name.
    Args period (int): Number of days for the analysis.
    Returns: list[dict[str, Any]]: List of dictionaries containing product names
    and their total sold quantities, sorted by volume.
    """
    try:
        date_limit = datetime.now() - timedelta(days=period)
        result = list(orders_col.aggregate([
            {"$match": {"date": {"$gte": date_limit}}},
            {"$unwind": "$products"},
            {
                "$group": {
                    "_id": "$products.name",
                    "total_sold": {"$sum": "$products.quantity"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "product": "$_id",
                    "total_sold": 1
                }
            },
            {
                "$sort": {"total_sold": -1}
            }
        ]))
        logger.info(f"{result}")
        return result
    except Exception as e:
        logger.error(f"Помилка визначення проданих товарів за період: {e}")
        raise


def get_orders_sum_by_user(user: str) -> list[dict[str, Any]]:
    """
    Calculates the lifetime total spend for a specific user.
    Args user (str): The unique username or identifier of the customer.
    Returns list[dict[str, Any]]: A list containing the user and their rounded
    total spend. Returns empty list if user not found.
    """
    try:
        result = list(orders_col.aggregate([
            {"$match": {"user": user}},
            {
                "$group": {
                    "_id": "$user",
                    "total_sum": {"$sum": "$total_price"}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "user": "$_id",
                    "total_sum": {"$round": ["$total_sum", 2]}
                }
            }
        ]))
        logger.info(f"{result}")
        return result

    except Exception as e:
        logger.error(f"Помилка обчислення суми по всім оформленим замовленням для '{user}': {e}")
        raise
