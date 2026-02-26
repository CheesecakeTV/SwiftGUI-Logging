import logging.handlers
import threading
import traceback
import sys
from typing import Callable, Any

try:
    import tkinter as tk
except ImportError:
    tk = None

def reroute_exceptions(
        logger: logging.Logger = logging.getLogger(),
        loglevel: int = logging.CRITICAL,
        *,
        logger_warnings: logging.Logger = None,
        loglevel_warnings: int = logging.WARNING,
        include_main_thread: bool = True,
        include_threads: bool = True,
        include_tkinter: bool = True,
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
    :param reraise: True, if the exception should be raised again. THIS DOESN'T WORK FOR THREAD EXCEPTIONS!
    :param include_main_thread: True, if the "normal thread's" exceptions should be caught
    :param include_threads: True, if Thread-exceptions should be caught too
    :param include_tkinter: True, if Tkinter-exceptions should be caught too
    :param pass_text_to_function: Pass a function/method and the exception-text is passed to it
    :param print_to_console: True, if the text should be printed to the console using print(...)
    :return:
    """
    if logger_warnings is None:
        logger_warnings = logger

    if loglevel_warnings is None:
        loglevel_warnings = loglevel

    def catch(exctype, value, tb, additional_text: str = ""):
        text = additional_text + "".join(traceback.format_exception(exctype, value, tb))

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

    def catch_normal(exctype, value, tb):
        catch(exctype, value, tb)
        if reraise:
            sys.__excepthook__(exctype, value, tb)

    def catch_thread(exc: threading.ExceptHookArgs):
        catch(exc.exc_type, exc.exc_value, exc.exc_traceback, f"On thread {exc.thread}:\n")

    if include_main_thread:
        sys.excepthook = catch_normal

    if include_threads:
        threading.excepthook = catch_thread

    if include_tkinter and tk is not None:
        # Catch tkinter exceptions
        actual_callback = tk.Tk.report_callback_exception
        def catch_tkinter(self, exctype, value, tb):
            catch(exctype, value, tb, additional_text="Tkinter exception:\n")

            if reraise:
                actual_callback(self, exctype, value, tb)   # I know this shows warnings, but it works

        tk.Tk.report_callback_exception = catch_tkinter




