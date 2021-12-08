import nox
from nox_poetry import Session, session

nox.options.stop_on_first_error = True
nox.options.error_on_external_run = True

python_versions = ["3.10", "3.9", "3.8", "3.7"]


@session(python=python_versions)
def testing(session: Session) -> None:
    """Run the test suite (using pytest)."""

    args = session.posargs or ["--cov"]
    session.install("pytest", "pytest-cov", "pytest-spec", "expects", ".")
    session.run("pytest", *args)
