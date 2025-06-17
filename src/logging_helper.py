import logging


def setup_logger():
    """Set up the logging configuration for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)-8s %(filename)s:%(lineno)4d %(message)s'
    )
