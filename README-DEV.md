# Quendor Development Notes

This document is entirely dedicated to me learning the Python ecosystem and documenting some of the logistics of developing this project in that ecosystem. These are more notes to myself about what I learned rather than anything that someone else needs to worry about.

## Python Versions to Support

I need to settle on some Python versions to support. I looked at the ["End of Life"](https://endoflife.date/python) page for Python versions.

For all versions, except the latest 3.9.x and 3.10.x variety, I focused on the last maintenance release made available. In those cases, that also referred to the versions that will have no further binaries deployed for them.

- Python 3.7.9: [https://www.python.org/downloads/release/python-379/](https://www.python.org/downloads/release/python-379/)
- Python 3.8.10: [https://www.python.org/downloads/release/python-3810/](https://www.python.org/downloads/release/python-3810/)

Python 3.9 and Python 3.10 are still both in active development so I expect I will update my versions of those peridocially. At the time of starting this document, and thus this project, I am using:

- Python 3.9.9: [https://www.python.org/downloads/release/python-399/](https://www.python.org/downloads/release/python-399/)
- Python 3.10.0: [https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)

I referenced the above with the planned release schedule for each version.

- Python 3.7 Release Schedule: [https://www.python.org/dev/peps/pep-0537/](https://www.python.org/dev/peps/pep-0537/)
- Python 3.8 Release Schedule: [https://www.python.org/dev/peps/pep-0569/](https://www.python.org/dev/peps/pep-0569/)
- Python 3.9 Release Schedule: [https://www.python.org/dev/peps/pep-0596/](https://www.python.org/dev/peps/pep-0596/)
- Python 3.10 Release Schedule: [https://www.python.org/dev/peps/pep-0619/](https://www.python.org/dev/peps/pep-0619/)

Release schedules are always on the [downloads page](https://www.python.org/downloads/).

## Developing on Multiple Python Versions

Project development will need some strategy for maintaining multiple Python versions on a given operating system.

### POSIX-based Systems

On a POSIX system this will be easy using [pyenv](https://github.com/pyenv/pyenv). With this tool in place, you can get a list of the versions you might want:

```
pyenv install --list | grep " 3\.[678910]"
```

You can then install the relevant versions:

```
pyenv install -v 3.7.9
pyenv install -v 3.8.10
pyenv install -v 3.9.9
pyenv install -v 3.10.0
```

For my local development on a POSIX system, I run the following command:

```
pyenv local 3.10.0 3.9.5 3.8.10 3.7.9
```

This is what generates a `.python-version` file. The first version listed in that command is the one that I intend primary development on.

### Windows Systems

If you use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install), you can essentially use a POSIX-like system. However, I also wanted to make sure that this wasn't entirely necessary for this project. On Windows, there is a similar tool to pyenv called [pyenv-win](https://github.com/pyenv-win/pyenv-win).

A challenge for Windows is that while pyenv-win works fine for basic stuff, when you get into tooling like Tox or Nox, it's not so great. Basically, when I started looking at it, the tool didn't support multiple version setup (see [issue 175](https://github.com/pyenv-win/pyenv-win/issues/175) and [issue 3](https://github.com/pyenv-win/pyenv-win/issues/3)). The latter issue seems to indicate the problem is fixed (possibly as part of [issue 217](https://github.com/pyenv-win/pyenv-win/pull/217)).

I will investigate that tool again but in the meantime I found that on Windows, you can just install multiple Python versions directly from the package binaries provided. The challenge there is that Nox and tools generally won't use what's called the ["py" launcher](https://www.python.org/dev/peps/pep-0397/). For the Nox problem, see [issue 250](https://github.com/theacodes/nox/issues/250) and [issue 233](https://github.com/theacodes/nox/issues/233). The latter issue indicates this may no longer be a problem anyway. That said, this may not matter based on the setup I was able to get working. I'll document here what I found to be generally workable on Windows.

If using Windows 10, you might want to remove its ability to go to the Microsoft Store when you use Python. You can do this on the settings page. Under "Apps and Features", you'll see "Manage App Execution Aliases" and there are some application execution aliases set up for you. You’ll want to turn off the "App Installer" aliases for Python.

Now install your Python versions just by using the binary distributions provided at the [Python downloads page](https://www.python.org/downloads/). These should be going to `AppData\Local` and on their own path: `Python\Python37`, `Python\Python38` and so on. You'll want to make sure you check the "Add Python to PATH" option. Once everything is installed, I then went to the following location:

```
cd %USERPROFILE%\appdata\local\programs\python
```

For each Python directory that was created here, you can do the following:

- Python 3.7: `copy python37\python.exe python37\python37.exe`
- Python 3.8: `copy python38\python.exe python38\python38.exe`
- Python 3.9: `copy python39\python.exe python39\python39.exe`
- Python 3.10: `copy python39\python.exe python39\python310.exe`

Then you'll want to edit your Environment Variables. Select "Path" in the "User Variables" section and make sure the following are in place in whatever order you want the Python versions to be:

- Python 3.10:
  - `%USERPROFILE%\appdata\local\programs\python\python310\scripts\`
  - `%USERPROFILE%\appdata\local\programs\python\python310\`

- Python 3.9:
  - `%USERPROFILE%\appdata\local\programs\python\python39\scripts\`
  - `%USERPROFILE%\appdata\local\programs\python\python39\`

- Python 3.8:
  - `%USERPROFILE%\appdata\local\programs\python\python38\scripts\`
  - `%USERPROFILE%\appdata\local\programs\python\python38\`

- Python 3.7:
  - `%USERPROFILE%\appdata\local\programs\python\python37\scripts\`
  - `%USERPROFILE%\appdata\local\programs\python\python37\`

Here I put the Python installations in the order that I cared about them, in terms of support for Quendor. If you need to access supporting tools, like pip, from a specific version, you can do this:

```
python38 -m pip install --upgrade pip
python39 -m pip install --upgrade pip
```

You can certainly also attempt to recreate a POSIX system on Windows, such as by using Cygwin or the Windows Subsystem for Linux. That being said, I rarely found that to be a workable option in terms of sustaining development, especially since you don't really need it. I felt I wouldn't be able to count on other developers who might work on the project wanting to go through all that if they were on Windows systems,especially when my own development approach suggested all of it wasn't necessary. So I tried for a least friction path here.

## Python Project Tooling

Quendor will need a Python package and dependency manager. I've found [Poetry](https://python-poetry.org/) to be extremely effective in this context and it works well on POSIX systems and Windows. The one thing I specifically run in the project is the following:

```
poetry config --local virtualenvs.in-project true
```

This way the virtual machines that are created for the project are created in the project directory. They are, of course, excluded from being version controlled.

Incidentally, if you need to uninstall Poetry, you can see [issue 644](https://github.com/python-poetry/poetry/issues/644) which seems to lead to [issue 2245](https://github.com/python-poetry/poetry/issues/2245).

Poetry creates a pyproject.toml file, which is a type of Python package configuration file specified in [PEP 517](https://www.python.org/dev/peps/pep-0517/) and [518](https://www.python.org/dev/peps/pep-0518/). The project configuration uses the [TOML](https://github.com/toml-lang/toml) syntax. One thing to note is that in this file I set the Python version in the `tool.poetry.dependencies` section to be the _minimum_ version I intend to support:

```
[tool.poetry.dependencies]
python = "^3.7"
```

## Project Structure

### To `src` or not to `src`?

Quendor will use a `src` directory.

When reading up on this topic of a high-level `src` directory, I came upon ["Testing & Packaging"](https://hynek.me/articles/testing-packaging/). The idea being conveyed here is that without a `src` directory, your tests do not run against the package _as it will be installed by its users_. Those tests instead run against whatever the situation in your project directory is.

Even removing the context of tests, the behavior of an application can change completely once you package and install it somewhere else. Users will be very unlikely to have the same current working directory as you do.

So the idea is that you isolate your code into a separate – _un-importable_ – directory, which is what `src` is. This serves as a constraint. This means you will be forced to test the installed code, essentially by installing in a virtual environment. This will ensure that the deployed code works when it's packaged correctly. This means you will be very unlikely to publish a broken distribution because you are testing the code how it will be in its distributed form. This also means you will be forced to install the distribution. This will surface missing modules or broken dependencies.

As part of researching all this, I came across ["Using the src layout for a Python package"](https://www.lukemiloszewski.com/blog/python-src-layout/) which further cemented my thinking to go this route.

## Project Testing

Certainly [pytest](https://docs.pytest.org/en/latest/) is the _de facto_ standard these days so I went with that. I wanted to use an expectations library rather than just rely on assertions so I use [expects](https://pypi.org/project/expects/) for that purpose. I also wanted the ability to provide specification output for test runs and for that I used [pytest-spec](https://pypi.org/project/pytest-spec/). Code coverage relative to the executed tests can be determined using [coverage](https://pypi.org/project/coverage/) so I include that but I also use the [pytest-cov](https://pypi.org/project/pytest-cov/) plugin. The plugin integrates coverage with pytest.

All [tests are placed outside of the application code](https://doc.pytest.org/en/latest/explanation/goodpractices.html#tests-outside-application-code) and the `tests` directory is treated as a package.

Basic tests can be run with:

```
poetry run pytest
```

To get the specification-based output, you can do this:

```
poetry run pytest --spec
```

To get the code coverage console report, you can do this:

```
poetry run pytest --cov
```

To generate an HTML report for the coverage, you can do this:

```
poetry run pytest --cov --cov-report html
```

I know a goal is to aim for 100% code coverage. In my case, I've started this project with a "fail under" option of 80%. What that means is that I must have at least 80% code coverage in order for my test suite to be considered passing.

With the project automation it is possible to run a single test module:

```
nox -- tests/test_quendor.py
```

## Project Automation

I decided to use [Nox](https://nox.thea.codes/en/stable/) for this project even though I know there is still a lot of momentum around using [tox](https://tox.wiki/en/latest/). I like how Nox uses a standard Python file for its configuration. I also use a tool called [nox-poetry](https://pypi.org/project/nox-poetry/) which, as its name would imply, provides some nice integration with Poetry and keeps the automation tasks looking nice and clean.

I do recommend installing these as "user" installs:

```
pip install --user --upgrade nox
pip install --user --upgrade nox-poetry
```

Using nox-poetry forces a reliance on [constraints files](https://pip.pypa.io/en/stable/user_guide/#constraints-files). These are created by using Poetry's ability to [export](https://python-poetry.org/docs/cli/#export). What this lets you do is use Poetry to manage all the various tools as development dependencies. So you can intall individual packages with `session.install` but then use the `poetry.lock` file to constrain their versions. This is what makes the build and testing process deterministic and repeatable.

It's worth noting that Nox recreates the virtual environments from scratch on each invocation. You can speed things up by passing the `--reuse-existing-virtualenvs` (`-r`) option. This option can also be set once in the `noxfile.py` but I find I generally prefer to follow the better practice of "fresh virtual environment" each time and only override that with the command line option when I feel the need to.

You can also specify `reuse_venv=True` in a given session for Nox by including that line in the session annotation.

You can always get a list of all the tasks that have been specified:

```
nox --list
```

## Project Code Quality

I'm using [flake8](https://pypi.org/project/flake8/) for this project. This kind of tools is an aggregator that brings together various linters and executes them. Each linter provides certain error codes. Out-of-the box you get the following linters:

* [pyflakes](https://pypi.org/project/pyflakes/); generates F codes
* [pycodestyle](https://pypi.org/project/pycodestyle/); generates W (warning) and E (error) codes; uses [PEP 8](https://www.python.org/dev/peps/pep-0008/)
* [mccabe](https://pypi.org/project/mccabe/); generates C codes

Using [flake8-codes](https://pypi.org/project/flake8-codes/) is a handy way to list out a lot of the codes that are generated.

```
poetry run python -m flake8_codes W
```

The flake8 tool is one that has consistently not moved to using the pyproject.toml for its configuration settings, even as an option. (See [issue 234](https://github.com/PyCQA/flake8/issues/234)). There are ways to do it but it seems easier to just use the `.flake8` file as part of the project and that's what I do here.

As of flake8 3.0, the `--select` option is a whitelist; this means checks not listed are being implicitly disabled. So if you use the option at all, then you have to explicitly specify all checks you want enabled.

There is something called [extend-select](https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-extend-select) but I haven't found that it's necessarily any better to provide extended selection than it is to just include all codes and selectively exclude specific codes when desired.

Using [flake8-html](https://pypi.org/project/flake8-html/) allows you to generate some nice HTML reporting.

## Project Code Formatting

I'm using [Black](https://pypi.org/project/black/) for this mainly because it's largely considered "uncompromising" and thus doesn't have a lot of configurability to work with. While formatting can be handled entirely separately from linting, I do feel that formatting is part of code quality. Thus I do use the [flake8-black](https://pypi.org/project/flake8-black/) plugin, which will effectively linter warnings if it detects that the Black formatter would have to make changes.

## Python Packages

As my project started building up and, more particularly, as I started to use a code editor like VS Code, I found I had to really understand how and where Python was getting its packages from.

### Listing Packages

The command `pip list` will get all installed packages; `pip list --user` will only get user-installed packages.

There is no way to use something like `pip list --system`. An [issue](https://github.com/pypa/pip/issues/4809) has been raised around that. That led to [another issue](https://github.com/pypa/pip/issues/5686) -- that seems of dubious relevance at all -- which in turn points to [yet another issue](https://github.com/pypa/pip/issues/4575). You can do this:

```
pip list --not-required
```

This will exclude packages that are required by another package, which does at least give you a slightly constrained list.

### Finding Site Packages

Global site-packages (apparently referred to as "dist-packages") directories are listed in `sys.path` when you run:

```
python -m site
```

For a more concise list run `getsitepackages` from the `site` module in Python code:

```
python -c 'import site; print(site.getsitepackages())'
```

The per user site-packages directory is where Python installs your local packages:

```
python -m site --user-site
```

Interestingly, Python currently uses [eight paths](https://docs.python.org/3/library/sysconfig.html#installation-paths). You can check any of these via a command in your operating system of choice. So for the "purelib", you can do the following:

- Linux: `python3 -c "import sysconfig; print(sysconfig.get_path('purelib'))"`
- MacOS: `python3 -c "import sysconfig; print(sysconfig.get_path('purelib'))"`
- Windows: `py -c "import sysconfig; print(sysconfig.get_path('purelib'))"`

The function `sysconfig.get_paths()` returns a dict of all of the relevant installation paths. From the Python REPL, you can see that:

```
>>> import sysconfig
>>> sysconfig.get_paths()
```

### Finding the Python Path

You can do the following to see what the current Python path actually is.

```
python -c "import sys; print('\n'.join(sys.path))"
```
