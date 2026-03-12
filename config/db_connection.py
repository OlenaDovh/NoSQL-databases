import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

import logging

logger = logging.getLogger(__name__)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    products_col = db["products"]
    orders_col = db["orders"]
    products_col.create_index("category")
    logger.info(f"Успішно підключено до бази даних: {DB_NAME}")
except (ConnectionFailure, ServerSelectionTimeoutError):
    logger.error(f"Помилка. Не вдалося підключитися до {DB_NAME}")
