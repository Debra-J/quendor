# Development Notes

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