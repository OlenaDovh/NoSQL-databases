from datetime import datetime, timedelta
from config.db_connection import orders_col
from pymongo.errors import PyMongoError
from models.orders import Order
import logging

logger = logging.getLogger(__name__)


def create_order(order: Order) -> dict:
    """Create a new order"""
    try:
        result = orders_col.insert_one(order.to_dict())
        logger.info(f"Order created | id={result.inserted_id}")
        return result
    except PyMongoError as e:
        logger.error(f"Database error while creating order: {e}")
        raise


def all_orders_for_last_period(period: int) -> list:
    """Returns all orders for last period days"""
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


def get_sold_products_count(period: int) -> list:
    """Returns sold products count"""
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


def get_orders_sum_by_user(user: str) -> list:
    """Returns orders sum by user"""
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
