from models.orders import Order
from services.product_operations import (get_product_price, get_product_count_in_stock, update_prods_in_stock)
from services.order_operations import create_order
from utils.order_generator import generate_order_num

import logging

logger = logging.getLogger(__name__)


def purchase_creation(user, products_with_count: dict) -> dict:
    """Returns dict with purchase details"""
    try:
        logger.info(f"Оформлення замовлення для '{user}'")
        total_price = 0
        products_list = []

        for product_name, count in products_with_count.items():
            stock = get_product_count_in_stock(product_name)
            if stock is None or stock < count:
                raise ValueError(f"Недостатньо '{product_name}' на складі (доступно: {stock})")

        for product_name, count in products_with_count.items():
            price = get_product_price(product_name)

            update_prods_in_stock(product_name, count, "remove")

            products_list.append({
                "name": product_name,
                "quantity": count,
                "price": price
            })
            total_price += price * count

        order = Order(
            order_number=generate_order_num(),
            user=user,
            products=products_list,
            total_price=round(total_price, 2)
        )

        create_order(order)

        logger.info(f"Замовлення {order.order_number} оформлено успішно. Загальна сума {order.total_price}")
        return order.to_dict()

    except Exception as e:
        logger.error(f"Помилка оформлення замовлення: {e}")
        raise
