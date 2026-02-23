import logging


def disable_root_handlers():
    """
    Remove all root handlers so the root handler does nothing.
    Useful when you want to generate the logging-system from ground up
    :return:
    """
    logging.getLogger().handlers.clear()
    logging.getLogger().addHandler(logging.NullHandler())

