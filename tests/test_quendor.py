"""Generic tests for Quendor execution."""

from expects import equal, expect


def test_report_package_version() -> None:
    """Package reports its current version."""

    import quendor

    expect(quendor.__version__).to(equal("0.1.0"))
