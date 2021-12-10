"""Command line interface module for Quendor."""

import argparse
import sys
import textwrap

import logzero

from quendor import __version__


def process_options(args: list) -> dict:
    """
    Process all arguments from the command line.

    An argument is a single part of a command line, delimited by blanks.
    An option is a particular type of argument (or a part of an argument).
    A parameter is a particular type of argument.

    An option generally modifies the behavior of the command line. A parameter
    generally provides additional information to a single option.

    This function places all options into a dictionary. This also handles the
    display of the options via the command line.

    Args:
        args: The arguments passed in via the command line.

    Returns:
        A dictionary of the arguments and any associated values.
    """

    parser = argparse.ArgumentParser(
        prog="quendor",
        description="Execute a z-code program on the Z-Machine",
        epilog=textwrap.dedent("""Enjoy your visit to Quendor!"""),
    )

    parser.add_argument(
        "zcode",
        action="store",
        type=str,
        help="z-code program to load",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        dest="loglevel",
        const=logzero.DEBUG,
        help="print debug logging",
    )

    parser.add_argument(
        "-i",
        "--info",
        action="store_const",
        dest="loglevel",
        const=logzero.INFO,
        help="print informative logging",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="version information",
    )

    if "-v" in args or "--version" in args:
        print(f"Version: {__version__}\n")
        sys.exit(0)

    options = parser.parse_args(args)

    return vars(options)
