import logging


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with a specified name.

    This function configures the logging format and level for the logger.
    It creates a logger instance with the provided name and sets its
    logging level to INFO.

    Parameters:
    name (str): The name of the logger to be created.

    Returns:
    logging.Logger: The configured logger instance.
    """
    msg_format = "%(asctime)s %(levelname)s %(name)s: %(message)s"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format=msg_format, datefmt=datetime_format)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
