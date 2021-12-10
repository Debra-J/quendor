"""Entry point module for the Quendor interpreter."""

import sys

from quendor.cli import process_options


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

    process_options(args)

    return 0
