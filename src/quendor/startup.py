"""Entry point module for the Quendor interpreter."""

import sys

from logzero import logger

from quendor.cli import process_options
from quendor.logging import setup_logging
from quendor.program import Program


def setup_quendor(cli: dict) -> None:
    """
    Establish the data Quendor will operate on.

    The goal of this function will be to make sure that Quendor is set up
    with a viable zcode program that can be executed.

    Args:
        cli: the parsed command line arguments
    """

    Program(cli["zcode"])


def main(args: list = None) -> int:
    """Entry point function for the Quendor interpreter."""

    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"

    if sys.version_info < (3, 7):
        sys.stderr.write("\nQuendor requires Python 3.7 or later.\n")
        sys.stderr.write(f"Your current version is {python_version}\n\n")
        sys.exit(1)

    print("\nQuendor Z-Machine Interpreter\n")

    if not args:
        args = sys.argv[1:]

    cli = process_options(args)

    setup_logging(cli["loglevel"])

    logger.debug(f"Argument count: {'':>4}" + str(len(args)))

    for i, arg in enumerate(args):
        logger.debug(f"Argument {i}: {'':>8}" + arg)

    logger.debug(f"Parsed arguments: {'':>2}" + f"{cli}")

    setup_quendor(cli)

    return 0
