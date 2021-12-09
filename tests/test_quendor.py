"""Generic tests for Quendor execution."""

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

    main()

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
