"""Generic tests for Quendor execution."""

import os
import sys
from unittest import mock

from expects import contain, equal, expect

import pytest


def test_report_package_version() -> None:
    """Package reports its current version."""

    import quendor

    expect(quendor.__version__).to(equal("0.1.0"))


def test_quendor_startup_banner(capsys: pytest.CaptureFixture) -> None:
    """Quendor provides a minimal banner."""

    from quendor.__main__ import main

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "test_program.z5")

    with mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main([file_path])

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain("Quendor Z-Machine Interpreter"))


def test_bad_python_version(capsys: pytest.CaptureFixture) -> None:
    """Quendor determines if minimal Python version is met."""

    from quendor.__main__ import main

    with mock.patch.object(sys, "version_info", (3, 5)), pytest.raises(
        SystemExit,
    ) as pytest_wrapped_e:
        main()

    terminal_text = capsys.readouterr()
    expect(terminal_text.err).to(contain("Quendor requires Python 3.7"))

    expect(pytest_wrapped_e.type).to(equal(SystemExit))
    expect(pytest_wrapped_e.value.code).to(equal(1))


def test_quendor_cli_version(capsys: pytest.CaptureFixture) -> None:
    """Quendor can report its version from the cli."""

    import quendor
    from quendor.__main__ import main

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["--version"])

    expect(pytest_wrapped_e.type).to(equal(SystemExit))
    expect(pytest_wrapped_e.value.code).to(equal(0))

    captured = capsys.readouterr()
    result = captured.out

    expect(result).to(contain(f"Version: {quendor.__version__}"))


def test_debug_logging(capsys: pytest.CaptureFixture) -> None:
    """Quendor can display debug log information."""

    from quendor.__main__ import main

    file_path = os.path.join(os.path.dirname(__file__), "./fixtures", "test_program.z5")

    with mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main([file_path, "-d"])

    captured = capsys.readouterr()
    result = captured.err

    expect(result).to(contain("Parsed arguments:"))


def test_startup_no_zcode(capsys: pytest.CaptureFixture) -> None:
    """Quendor must be started with a zcode program specified."""

    from quendor.__main__ import main

    with pytest.raises(SystemExit) as pytest_wrapped_e, mock.patch.object(
        sys,
        "argv",
        [""],
    ):
        main()

    expect(pytest_wrapped_e.type).to(equal(SystemExit))
    expect(pytest_wrapped_e.value.code).to(equal(2))

    captured = capsys.readouterr()
    result = captured.err

    expect(result).to(contain("the following arguments are required: zcode"))
