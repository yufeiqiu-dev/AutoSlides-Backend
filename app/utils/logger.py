import logging
import os

def get_logger(name: str = "AutoSlides"):
    """Return a configured logger with a consistent format."""
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Set log format
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
