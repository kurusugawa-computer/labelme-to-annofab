import logging

logger = logging.getLogger(__name__)


def set_logger() -> None:
    logging_formatter = "%(levelname)-8s : %(asctime)s : %(name)s : %(message)s"
    logging.basicConfig(format=logging_formatter)
    logging.getLogger("pandasetutils").setLevel(level=logging.DEBUG)
    logging.getLogger("__main__").setLevel(level=logging.DEBUG)
