import nox
from nox_poetry import Session, session

nox.options.stop_on_first_error = True
nox.options.error_on_external_run = True
nox.options.sessions = "formatting", "linting", "testing"

python_versions = ["3.10", "3.9", "3.8", "3.7"]
locations = "src", "tests", "noxfile.py"


@session(python=python_versions)
def testing(session: Session) -> None:
    """Run the test suite (using pytest)."""

    args = session.posargs or ["--cov"]
    session.install("pytest", "pytest-cov", "pytest-spec", "expects", ".")
    session.run("pytest", *args)


@session
def linting(session: Session) -> None:
    """Run linting checks (using flake8)."""

    args = session.posargs or locations
    session.install("flake8", "flake8-black")
    session.run("flake8", *args)


@session
def lintreport(session: Session) -> Session:
    """Generate linting HTML report."""

    list_locations = list(locations)
    list_locations.insert(0, "--format=html")

    session.posargs = tuple(list_locations)

    session.install("flake8-html")

    linting(session)


@session
def formatting(session: Session) -> None:
    """Run formatter (using black)."""

    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)
