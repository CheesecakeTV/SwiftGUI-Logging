import SwiftGUI_Logging as sgl
from pathlib import Path
import logging
from datetime import datetime as dt
import io
import shutil

def exceptions_to_file(
        filepath: str | Path,
        logger: str | logging.Logger = "",
        buffer_size: int = 5000,
        trigger_level: int = logging.ERROR,
        log_level: int = logging.DEBUG,
        reraise: bool = False,
        datetime_format: str = "_%Y-%m-%d_%H-%M-%S",
        formatter_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
):
    """
    Buffers the last n logging-entries.
    If the program executes as expected, nothing happens.
    If an exception crashes the program, the whole buffer is logged to a file, including the exception.

    This is also true if the logger receives a report of loglevel higher than the specified trigger.

    Every filesave generates its own file with a timestamp in the name.

    :param filepath: Path to a log-file WITHOUT THE TIMESTAMP. The timestamp is added at the end before the suffix.
    :param logger: You can specify which logger should receive the exception-logs.
    :param buffer_size: How many reports are saved before the first ones are overritten again
    :param trigger_level: Level at which the exceptions are treated. Reports at and above this level trigger a file-write
    :param log_level: Logs below this level are ignored and not written to the file
    :param reraise: True, if the exception should still be raised, even though it was logged. Good for debugging purposes
    :param datetime_format: Format of the timestamp that extends the filename
    :param formatter_format: Format of the log-entries in the file
    :return:
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    filepath = filepath.parent / (filepath.stem + dt.now().strftime(datetime_format) + filepath.suffix)

    if isinstance(logger, str):
        logger = logging.getLogger(logger)

    logger.setLevel(log_level)

    stream = io.StringIO()
    stream_handler = logging.StreamHandler(stream)
    stream_handler.setFormatter(
        logging.Formatter(formatter_format)
    )
    buffer_handler = sgl.MemoryHandlerRotatingBuffer(buffer_size, trigger_level, target=stream_handler)

    logger.addHandler(buffer_handler)

    def exception_occured(*_):
        stream.seek(0)
        if not stream.read(1):
            # Nothing to report
            print("Nothing to report")
            return

        with open(filepath, "w") as f:
            stream.seek(0)
            #f.write(stream.read())
            shutil.copyfileobj(stream, f)

    sgl.reroute_exceptions(logger, reraise=reraise, loglevel=trigger_level, pass_text_to_function=exception_occured)

