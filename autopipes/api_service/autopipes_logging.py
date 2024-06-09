import logging
import os


def get_logger(name: str = "root"):
    autopipes_logging = os.getenv("AUTOPIPES_LOGGING")

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=autopipes_logging,
    )
    logger = logging.getLogger(name)
    return logger
