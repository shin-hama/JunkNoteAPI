import logging

from app.core.logger import setup_logger

logger = logging.getLogger(__name__)
setup_logger()


def test():
    logger.info("test")
