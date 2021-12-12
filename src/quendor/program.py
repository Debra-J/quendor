"""Module for zcode program abstraction."""

import os
from pathlib import Path

from logzero import logger

from quendor.errors import (
    UnableToAccessZcodeProgramError,
    UnableToLocateZcodeProgramError,
)


class Program:
    """Abstraction for a zcode program."""

    def __init__(self, program: str) -> None:
        self._program: str = program
        self.file: str = ""
        self.data: bytes = b""

        self._locate()
        self._read_memory()

    def _locate(self) -> None:
        """Determine if a zcode program exists."""

        paths = [os.curdir]
        paths.append(str(Path(os.path.expandvars("$ZCODE_PATH"))))

        for path in paths:
            found = os.path.isfile(os.path.join(path, self._program))

            if found:
                self.file = os.path.join(path, self._program)

                logger.debug(f"zcode program file: {self.file}")

                return

        raise UnableToLocateZcodeProgramError(
            f"Quendor was unable to find the zcode program.\n\nChecked in: {paths}",
        )

    def _read_memory(self) -> None:
        """
        Read zcode program memory.

        Memory in the context of a zcode program is a simply a serialiation
        of state, encoded as binary data. How that data is read from the
        zcode program depends on what format of program it is.
        """

        self._read_data()

    def _read_data(self) -> None:
        """Open a program file and read binary contents."""

        try:
            with open(self.file, "rb") as zcode_program:
                self.data = zcode_program.read()
        except OSError as exc:
            raise UnableToAccessZcodeProgramError(
                f"Unable to access the zcode program: {self.file}",
            ) from exc
