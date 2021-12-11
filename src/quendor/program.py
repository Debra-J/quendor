"""Module for zcode program abstraction."""

import os
from pathlib import Path

from logzero import logger

from quendor.errors import UnableToLocateZcodeProgramError


class Program:
    """Abstraction for a zcode program."""

    def __init__(self, program: str) -> None:
        self._program: str = program
        self.file: str = ""

        self._locate()

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
