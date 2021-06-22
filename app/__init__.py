import logging

__version__ = "0.1.0"


def setup_logger() -> None:
    from app.core.config import LOGGING_LEVEL

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    logger.setLevel(LOGGING_LEVEL)


setup_logger()
