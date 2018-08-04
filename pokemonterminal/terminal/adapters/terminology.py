from os import environ
from subprocess import run

from . import TerminalProvider as _TProv


class TerminologyProvider(_TProv):
    @staticmethod
    def is_compatible() -> bool:
        return environ.get("TERMINOLOGY") == '1'

    @staticmethod
    def change_terminal(path: str):
        run(["tybg", path], check=True)

    @staticmethod
    def clear():
        run("tybg", check=True)

    def __repr__(self):
        return "Terminology"
