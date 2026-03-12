import logging
import sys


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s | %(name)s | %(funcName)s",
        stream=sys.stdout
    )


setup_logger()
logger = logging.getLogger(__name__)
