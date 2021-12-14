"""
Z-Code Story File Analyzer.

This module provides functionality to analyze z-code story files by
running `txd` or `infodump` against the binary story files in order
to generate assembly information.
"""

import argparse
import os
import pathlib
import subprocess
import sys
import textwrap

import colorama

from termcolor import colored

if sys.version_info < (3, 7):
    sys.stderr.write("This script requires at least version 3.7 of Python.\n")
    sys.exit(1)

colorama.init()


def process_parameters(params: list) -> dict:
    """Process all parameters from the command line."""

    parser = argparse.ArgumentParser(
        description="Quendor Z-Machine Resource Analyzer",
        usage=textwrap.dedent(
            """
            The general format is:

                analyzer <action>

            Examples:
                (1) analyzer --txd <zcode_file>
                    - run z-code disassembler against a story file

                (2) analyzer --infodump <zcode_file>
                    - run table parser against a story file
            """,
        ),
        epilog=textwrap.dedent(
            """
            Enjoy your story research!
            """,
        ),
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--txd",
        nargs=1,
        dest="txd",
        metavar="zcode_file",
        help="Run the TXD tool against a story file.",
    )
    group.add_argument(
        "--infodump",
        nargs=1,
        dest="infodump",
        metavar="zcode_file",
        help="Run the Infodump tool against a story file.",
    )

    param_set = parser.parse_args()

    return vars(param_set)


def check_for_tool(tool_name: str) -> None:
    """Check if analysis tool is present on the file system."""

    if sys.platform in ["win32", "msys", "cygwin"]:
        tool_name += ".exe"

    if pathlib.Path(f"./resources/ztools/{tool_name}").is_file():
        return

    sys.stderr.write(
        colored(
            f"The tool `{tool_name}` was not found in `resources\\ztools`.\n"
            "You can download this tool using the `downloader.py` script.\n\n",
            "red",
        ),
    )


def check_for_story(story_file: str) -> None:
    """Check if story file is present on the file system."""

    # The story path will either default to using the `resources`
    # directory of the current project or will respect whatever
    # path was passed in with the file.
    if os.path.dirname(story_file) == "":
        story_path = f"./resources/zcode/{story_file}"
    else:
        story_path = f"./{story_file}"

    if pathlib.Path(story_path).is_file():
        return

    sys.stderr.write(
        colored(f"The story file `{story_file}` was not found.\n\n", "red"),
    )


def run_tool(name: str, story_file: str) -> list:
    """Execute the provided tool against the provided story file."""

    # The tool_name will be the actual name of the tool as it appears
    # on the file system. The name will be the name that was passed in.
    # This is to account for the naming difference of the files on
    # different operating systems.
    tool_name = name

    if sys.platform in ["win32", "msys", "cygwin"]:
        tool_name += ".exe"

    # The story path will either default to using the `resources`
    # directory of the current project or will respect whatever
    # path was passed in with the file.
    if os.path.dirname(story_file) == "":
        story_path = f"./resources/zcode/{story_file}"
    else:
        story_path = f"./{story_file}"

    check_for_story(story_path)

    if name == "txd":
        return run_command(f"./resources/ztools/{tool_name}", "andw0", story_path)

    if name == "infodump":
        return run_command(f"./resources/ztools/{tool_name}", "fw0", story_path)

    return []


def run_command(tool: str, options: str, story_file: str) -> list:
    """
    Run a tool command.

    This function runs a specified tool with any associated options.
    The output of the tool will be captured and returned.

    Args:
        tool: the ztool to run
        options: the command line options to pass to the ztool
        story_file: the zcode program to run the tool against

    Returns:
        the output from running the ztool against a zcode program
    """

    pathlib.Path("resources/zdata").mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        args=[tool, f"-{options}", story_file],
        universal_newlines=True,
        stdout=subprocess.PIPE,
        check=True,
    )

    return result.stdout.splitlines(True)


def process(output: list, tool: str, story_file: str) -> None:
    """
    Process tool output.

    This function makes sure that all output files are processed so that
    newlines are handled correctly.

    Args:
        output: the command line output from a ztool
        tool: the ztool that provided the output
        story_file: the zcode program the ztool was run on
    """

    print(colored("Generating: ", "yellow"), end="")
    print(colored(f"{story_file}_{tool}.txt", "cyan"))

    with open(f"./resources/zdata/{story_file}_{tool}.txt", "w") as output_file:
        output_file.writelines(output)
        output_file.close()

    print(colored("Success!", "green"))


def main(params: list = None) -> int:
    """Entry point for the Quendor analyzer."""

    print("\nQuendor Z-Machine Resource Analyzer\n")

    if not params:
        params = sys.argv[1:]

    arg_set = process_parameters(params)

    for tool, value in arg_set.items():
        if type(value) is list:
            check_for_tool(tool)
            output = run_tool(tool, value[0])
            process(output, tool, os.path.basename(value[0]))

    return 0


if __name__ == "__main__":
    main()
