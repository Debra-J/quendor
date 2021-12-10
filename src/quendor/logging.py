"""Logging module for the Quendor interpreter."""

import logzero


def setup_logging(log_level: int) -> None:
    """
    Provide logger settings.

    Logging levels:

    - CRITICAL: 50
    - ERROR: 40
    - WARNING: 30
    - INFO: 20
    - DEBUG: 10
    - NOTSET: 0

    Args:
        log_level: the level of logging to display.
    """

    if not log_level:
        log_level = logzero.ERROR

    log_format = (
        "%(color)s[%(levelname)1.7s %(module)s:%(lineno)d]" "%(end_color)s %(message)s"
    )

    formatter = logzero.LogFormatter(fmt=log_format)
    logzero.setup_default_logger(formatter=formatter)
    logzero.loglevel(log_level)
