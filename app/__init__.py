import logging


__version__ = "0.1.0"


def setup_logger() -> None:
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    logger.setLevel(logging.DEBUG)


setup_logger()
