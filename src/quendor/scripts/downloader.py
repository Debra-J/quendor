"""
Z-Code Resource Downloader.

This module provides a way to acquire z-code story files from a targeted
repository on GitHub. This module can also download certain tools and
checker programs that help in the construction and/or testing of a
Z-Machine interpreter. Also possible is downloading the source code of
certain z-code programs since that source code can help understand how
certain instructions are being carried out as the z-code executes.
"""

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import textwrap
import zipfile

import colorama

import requests

from termcolor import colored

if sys.version_info < (3, 7):
    sys.stderr.write("This script requires at least version 3.7 of Python.\n")
    sys.exit(1)

colorama.init()

GIT_URL = "https://raw.github.com/"
GIT_USER = "jeffnyman/"
GIT_REPO = "zcode_catalog/"
GIT_BRANCH = "master/"

CHECKERS = [
    "crashme.z5",
    "czech.z5",
    "etude.z5",
    "gntests.z5",
    "praxix.z5",
    "random.z5",
    "strictz.z5",
    "unicode.z5",
    "ziptest-r13-s890619.z6",
    "ziptest-r40-s840613.z3",
]

ZORK_LIST = ["beyondzork", "zork0", "zork1", "zork2", "zork3", "minizork"]
Z3_LIST = [
    "ballyhoo",
    "cutthroats",
    "deadline",
    "enchanter",
    "hitchhiker",
    "hollywood",
    "hypochondriac",
    "infidel",
    "leathergoddesses",
    "lurkinghorror",
    "moonmist",
    "planetfall",
    "plunderedhearts",
    "restaurant",
    "seastalker",
    "sorcerer",
    "spellbreaker",
    "starcross",
    "stationfall",
    "suspect",
    "suspended",
    "witness",
    "wishbringer",
]
Z4_LIST = ["amfv", "bureaucracy", "nordandbert", "trinity"]
Z5_LIST = ["border_zone", "sherlock"]
Z6_LIST = ["abyss", "arthur", "journey", "shogun"]

INFORM_LIST = [
    "aug4.z8",
    "awaken.z5",
    "balances.z5",
    "bluechairs.z5",
    "bomber.z5",
    "delusions.z5",
    "destruct.z1",
    "devours.z5",
    "dreamhold.z8",
    "edifice.z5",
    "fade.z1",
    "freefall.z5",
    "green.z2",
    "huntdark.z5",
    "jigsaw.z8",
    "magic-toyshop.z5",
    "minster.z5",
    "tangle.z5",
    "varicella.z8",
    "vespers.z8",
    "wumpuz.z5",
    "wurm.z5",
    "zlife.z5",
    "zombies.z5",
    "zracer.z5",
    "zsnake.z5",
    "ztornado.z5",
    "ztrek.z5",
]


def process_parameters(params: list) -> dict:
    """Process all parameters from the command line."""

    parser = argparse.ArgumentParser(
        description="Quendor Z-Code Resource Downloader",
        usage=textwrap.dedent(
            """
        The general format is:

            quend <action>

        Examples:
            (1) quend --zcode <file>
                - downloads a z-code program

            (2) quend --listing
                - provides a listing of z-code programs in the repository

            (3) quend --tools
                - downloads a set of tools to analyze z-code files

            (4) quend --checkers
                - downloads a set of z-code checker files

            (5) quend --zsource <file>
                - downloads source code for a z-code program
        """,
        ),
        epilog=textwrap.dedent(
            """
            Enjoy your stories!
            """,
        ),
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--listing",
        action="store_true",
        help="provides list of resources",
    )
    group.add_argument(
        "--tools",
        action="store_true",
        help="provides tools for z-code analysis",
    )
    group.add_argument(
        "--checkers",
        action="store_true",
        help="provides z-code test files",
    )
    group.add_argument(
        "--zcode",
        nargs=1,
        dest="zcode",
        help="downloads a z-code program",
    )
    group.add_argument(
        "--zsource",
        nargs=1,
        dest="zsource",
        help="downloads source for a z-code program",
    )

    return vars(parser.parse_args())


def provide_listing() -> None:
    """
    Provide z-code resource list.

    This function will generate a listing of the z-code resources that are
    available at a targeted repository.
    """

    contents_url = GIT_URL + GIT_USER + GIT_REPO + GIT_BRANCH + "contents.txt"

    response = requests.get(contents_url)
    print(response.text)

    del response


def provide_tools() -> None:
    """
    Provide a set of z-code tools.

    This function will start the process of downloading tools that are
    available at a targeted zcode repository. These tools are useful in
    the analysis of zcode-programs.
    """

    windows_tools = ["txd.exe", "infodump.exe"]
    posix_tools = ["txd", "infodump"]

    tool_url = GIT_URL + GIT_USER + GIT_REPO + GIT_BRANCH + "ztools/"

    if sys.platform in ["win32", "msys", "cygwin"]:
        for tool in windows_tools:
            download_resource("ztools", tool_url, tool)
    elif sys.platform == "darwin" or sys.platform.startswith("linux"):
        for tool in posix_tools:
            download_resource("ztools", tool_url, tool)


def provide_checkers() -> None:
    """
    Provide a set of z-code checkers.

    These z-code files were designed specifically to test a specific
    interpreter implementations to determine how well they adhere to
    the Z-Machine specification or at least subsets of it.
    """

    checker_url = GIT_URL + GIT_USER + GIT_REPO + GIT_BRANCH + "zcheckers/"

    for checker in CHECKERS:
        download_resource("zcheckers", checker_url, checker)


def provide_zcode(zcode_type: str, zcode_file: str) -> None:
    """
    Provide a z-code program file.

    This function will provide a specific zcode program file file by
    downloading the specified file from a targeted zcode repository.

    Args:
        zcode_type (str): Value will be "zcode" or "zsource"
        zcode_file (str): Name of the resource to retrieve
    """

    zcode_url = GIT_URL + GIT_USER + GIT_REPO + GIT_BRANCH
    zcode_file = zcode_file[0]

    if zcode_file.endswith("zblorb"):
        download_resource(zcode_type, zcode_url + "zblorb/", zcode_file)
        return

    if zcode_file.endswith(("blb", "ulx", "gblorb")):
        download_resource(zcode_type, zcode_url + "glulx/", zcode_file)
        return

    for name in INFORM_LIST:
        if zcode_file.startswith(name):
            download_resource(zcode_type, zcode_url + "inform/", zcode_file)
            return

    for name in ZORK_LIST + Z3_LIST + Z4_LIST + Z5_LIST + Z6_LIST:
        if zcode_file.startswith(name):
            download_resource(zcode_type, zcode_url + f"{name}/", zcode_file)
            return

    sys.stderr.write(
        colored(
            f"The {zcode_type} {zcode_file} does not have a known starting point.\n\n",
            "red",
            attrs=["bold"],
        ),
    )


def download_resource(resource: str, resource_url: str, resource_name: str) -> None:
    """Download resources."""

    if pathlib.Path(f"./resources/{resource}/{resource_name}").is_file():
        print(colored(f"Skipping: {resource_name}; already exists.", "yellow"))
        return

    resource_url += resource_name

    response = requests.get(resource_url, stream=True)

    print(colored("Attempting to download: ", "yellow"), end="")
    print(colored(f"{resource_url}", "cyan"))

    if response.status_code == 200:
        provide_resource(resource, resource_name, response)
    else:
        sys.stderr.write(
            colored(
                f"Unable to locate {resource} resource: {resource_name}.\n",
                "red",
                attrs=["bold"],
            ),
        )

    # Source file archives should be removed.
    if resource == "zsource":
        try:
            os.remove(f"./resources/{resource}/{resource_name}")
        except OSError:
            sys.stderr.write(
                colored(
                    "Unable to remove zipped source file.\n",
                    "red",
                    attrs=["bold"],
                ),
            )

    del response


def provide_resource(
    resource: str,
    resource_name: str,
    response: requests.models.Response,
) -> None:
    """Provide a resource on the file system in an appropriate format."""

    pathlib.Path(f"resources/{resource}").mkdir(parents=True, exist_ok=True)

    with open(f"./resources/{resource}/{resource_name}", "wb") as resource_output:
        response.raw.decoded_content = True
        shutil.copyfileobj(response.raw, resource_output)

        # Any ztools will need to be executable.
        if resource == "ztools":
            command = f"chmod u+x ./resources/{resource}/{resource_name}"
            subprocess.Popen(command.split(), stdout=subprocess.PIPE)

        # Source files have to be unzipped.
        if resource == "zsource":
            try:
                if zipfile.is_zipfile(f"./resources/{resource}/{resource_name}"):
                    with zipfile.ZipFile(
                        f"./resources/{resource}/{resource_name}",
                        "r",
                    ) as zip_ref:
                        zip_ref.extractall(f"./resources/{resource}")
            except OSError:
                sys.stderr.write(
                    colored(
                        "Source file downloaded but it was not a zip file.\n",
                        "red",
                        attrs=["bold"],
                    ),
                )

        print(colored("Success!", "green"))


def process_action(action: str, value: str) -> None:
    """Process the action provided at the command line."""

    if action == "listing":
        provide_listing()
    elif action == "tools":
        provide_tools()
    elif action == "checkers":
        provide_checkers()
    elif action in ["zcode", "zsource"]:
        provide_zcode(action, value)


def main(args: list = None) -> int:
    """Entry point for the Quendor downloader."""

    print("\nQuendor Z-Code Resource Downloader\n")

    if not args:
        args = sys.argv[1:]

    arg_set = process_parameters(args)

    for action, value in arg_set.items():
        if value:
            process_action(action, value)

    return 0


if __name__ == "__main__":
    sys.exit(main())
