Quendor
=======

.. toctree::
    :hidden:
    :maxdepth: 1

    license
    reference

Quendor is a `Z-Machine <https://en.wikipedia.org/wiki/Z-machine>`_ emulator and interpreter.

Usage
-----

.. code-block:: console

    $ quendor [OPTIONS] zcode_program

.. option:: -d

    Provide debug logging as Quendor executes.

.. option:: -i

    Provide information logging as Quendor executes.

    Note that running logging with just `-i` shows only info.
    Running logging with `-d` shows info and debug.

.. option:: -v, --version

    Display the version and exit.

.. option:: -h, --help

    Display information about Quendor usage and arguments.
