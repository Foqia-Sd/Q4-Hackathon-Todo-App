import logging
import sys
from pythonjsonlogger import jsonlogger
from typing import Optional
import os

def setup_logger(name: str, log_level: Optional[str] = None) -> logging.Logger:
    """
    Set up a structured JSON logger
    """
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Prevent adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Create handler
    handler = logging.StreamHandler(sys.stdout)

    # Create formatter
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Global logger instance
app_logger = setup_logger(__name__)