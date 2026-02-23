import logging.handlers
import traceback
import sys
from typing import Callable, Any


def reroute_exceptions(
        logger: logging.Logger = logging.getLogger(),
        loglevel: int = logging.CRITICAL,
        *,
        logger_warnings: logging.Logger = None,
        loglevel_warnings: int = logging.WARNING,
        reraise: bool = False,
        print_to_console: bool = False,
        pass_text_to_function: Callable[[str], Any] = None,
):
    """
    Catch all unhandled exceptions and log them

    :param logger: The logger where EXCEPTIONS go
    :param loglevel: The loglevel for EXCEPTIONS
    :param logger_warnings: The logger where WARNINGS go
    :param loglevel_warnings: The level of logging for WARNINGS
    :param reraise: True, if the exception should be raised again
    :param pass_text_to_function: Pass a function/method and the exception-text is passed to it
    :param print_to_console: True, if the text should be printed to the console using print(...)
    :return:
    """
    if logger_warnings is None:
        logger_warnings = logger

    if loglevel_warnings is None:
        loglevel_warnings = loglevel

    def catch(exctype, value, tb):
        text = "".join(traceback.format_exception(exctype, value, tb))

        if issubclass(exctype, Warning):    # Warnings
            if logger_warnings is not None:
                logger_warnings.log(
                    loglevel_warnings,
                    text,
                )
        elif issubclass(exctype, Exception):    # Real exceptions
            if logger is not None:
                logger.log(
                    loglevel,
                    text,
                )
        else:
            # Keyboard interrupts and such
            sys.__excepthook__(exctype, value, tb)
            return  # Not really necessary

        if pass_text_to_function:
            pass_text_to_function(text)

        if print_to_console:
            print(text)

        if reraise:
            sys.__excepthook__(exctype, value, tb)

    sys.excepthook = catch
