import logging
import sys


def setup_logger() -> None:
    """
    Configures the root logger for the application.
    Sets the logging level to INFO, defines a structured format including
    timestamp, log level, message, logger name, and function name,
    and redirects the output to the standard output stream.
    Returns None
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s | %(name)s | %(funcName)s",
        stream=sys.stdout
    )


setup_logger()
logger = logging.getLogger(__name__)
