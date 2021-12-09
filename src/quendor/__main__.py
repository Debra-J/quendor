"""Package entry point for the Quendor interpreter."""

import sys


def main() -> int:
    """Entry point function for the Quendor interpreter."""

    python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"

    if sys.version_info < (3, 7):
        sys.stderr.write("\nQuendor requires Python 3.7 or later.\n")
        sys.stderr.write(f"Your current version is {python_version}\n\n")
        sys.exit(1)

    print("\nQuendor Z-Machine Interpreter\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
