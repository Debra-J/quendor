"""Module for zcode program abstraction."""

import os
from pathlib import Path

from logzero import logger

from quendor.errors import (
    InvalidZcodeProgramFormatError,
    UnableToAccessZcodeProgramError,
    UnableToLocateZcodeProgramError,
    UnknownZCodeProgramFormatError,
    UnsupportedZcodeProgramTypeError,
)


class Program:
    """Abstraction for a zcode program."""

    def __init__(self, program: str) -> None:
        self._program: str = program
        self.file: str = ""
        self.data: bytes = b""
        self.format: str = ""

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
        self._read_format()

    def _read_data(self) -> None:
        """Open a program file and read binary contents."""

        try:
            with open(self.file, "rb") as zcode_program:
                self.data = zcode_program.read()
        except OSError as exc:
            raise UnableToAccessZcodeProgramError(
                f"Unable to access the zcode program: {self.file}",
            ) from exc

    def _read_format(self) -> None:
        """
        Read the format of program file.

        This method will initially read the first four bytes. This will be
        enough to get the format for any valid program file. If the file is
        a blorb file then those first four bytes will indicate a group ID.
        If the file is an unblorbed zcode program then the first byte will
        indicatea Z-Machine version. However, the first byte will always
        indicate the version, even for a blorbed zcode program. So it's
        necessary to determine what specific format is being dealt with.

        Currently Quendor will not handle Glulx files at all.

        Raises:
            UnsupportedZcodeProgramTypeError: if a Glulx progam is loaded
            InvalidZcodeProgramFormatError: if invalid IFF program is loaded
            UnknownZCodeProgramFormatError: if zcode or blorb format not found
        """

        format_id = self.data[0:4]

        # Rule out Glulx right away since Quendor doesn't support it.

        if format_id.decode("latin-1").upper() == "GLUL":
            raise UnsupportedZcodeProgramTypeError(
                "Quendor cannot interpret Glulx files.",
            )

        # Determine if we have IFF file next and then determine if
        # we have an interactive fiction type of IFF file.

        if format_id.decode("latin-1") == "FORM":
            ifrs_id = self.data[8:12]

            if ifrs_id.decode("latin-1") != "IFRS":
                raise InvalidZcodeProgramFormatError(
                    "Quendor did not find an IFRS format type."
                    + f"\n\nFormat found was: {ifrs_id!r}",
                )
            else:
                self.format = "BLORB"
                logger.debug(f"zcode file format: {self.format}")
                return

        # If we got to this point, we likely have an unblorbed zcode file.

        if format_id[0] >= 1 and format_id[0] <= 8:
            self.format = "ZCODE"
            logger.debug(f"zcode file format: {self.format}")
            return

        raise UnknownZCodeProgramFormatError(
            f"Quendor cannot determine the file format of {self.file}",
        )
