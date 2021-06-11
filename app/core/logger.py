import logging


logger = logging.getLogger('app')


def setup_logger() -> None:
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    logger.setLevel(logging.DEBUG)

    logger.debug("setup logger")
