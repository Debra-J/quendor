"""Module for zcode program abstraction."""

from dataclasses import dataclass


@dataclass
class Program:
    """Abstraction for a zcode program."""

    def __init__(self, program: str) -> None:
        self._program: str = program
