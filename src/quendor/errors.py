"""Error repository module for Quendor-specific exceptions."""

import inspect
import ntpath
import sys

from termcolor import colored


class QuendorError(Exception):
    """Raise Quendor-specific execption."""

    def __init__(self, msg: str) -> None:
        try:
            source_name = inspect.currentframe().f_back.f_code.co_name  # type: ignore
            source_file = ntpath.basename(
                inspect.currentframe().f_back.f_code.co_filename,  # type: ignore
            )
            source_line = sys.exc_info()[-1].tb_lineno  # type: ignore
        except AttributeError:
            source_line = inspect.currentframe().f_back.f_lineno  # type: ignore

        error = colored(type(self).__name__, "red", attrs=["bold"])
        msg = colored(msg, "red", attrs=["bold"])
        source_name = colored(source_name, "yellow")
        source_file = colored(source_file, "yellow")

        self.args = (
            "\nQuendor Problem: {0}\nOccurred in: {1} in {2} (line {3})\n{4}\n".format(
                error,
                source_name,
                source_file,
                source_line,
                msg,
            ),
        )

        sys.exit(self)


class InvalidZcodeProgramFormatError(QuendorError):
    """Raise for a program with an non-IFRS format."""


class UnableToAccessZcodeProgramError(QuendorError):
    """Raise for a zcode program file that cannot be opened or read from."""


class UnableToLocateZcodeProgramError(QuendorError):
    """Raise for a zcode program file that cannot be located."""


class UnsupportedZcodeProgramTypeError(QuendorError):
    """Raise for a zcode program that cannot be interpreted."""
