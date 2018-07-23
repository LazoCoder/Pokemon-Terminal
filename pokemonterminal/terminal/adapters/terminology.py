from os import environ
from subprocess import run

from . import TerminalProvider as _TProv


class TerminologyProvider(_TProv):
    def is_compatible() -> bool:
        return environ.get("TERMINOLOGY") == '1'

    def change_terminal(path: str):
        run(["tybg", path], check=True)

    def clear():
        run("tybg", check=True)

    def __str__():
        return "Terminology"