import os
import pathlib
from configparser import ConfigParser
from typing import Union

import psutil

from . import TerminalProvider as _TProv


class Xfce4TerminalProvider(_TProv):
    @staticmethod
    def __set_bg_image(new: Union[os.PathLike, str]):
        path = pathlib.Path(
            os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        ) / 'xfce4' / 'terminal' / 'terminalrc'
        terminalrc = ConfigParser()
        terminalrc.optionxform = str
        terminalrc.read(path)
        terminalrc['Configuration'].update({'BackgroundImageFile': f'{new}'})
        with open(path, 'w') as f:
            terminalrc.write(f)

    @staticmethod
    def is_compatible() -> bool:
        ancestors = []
        proc = psutil.Process()
        while (proc := proc.parent()) is not None:
            ancestors.append(proc.name())
        return any(['xfce4' in p for p in ancestors])

    @staticmethod
    def clear():
        Xfce4TerminalProvider.__set_bg_image('')

    @staticmethod
    def change_terminal(path: str):
        Xfce4TerminalProvider.__set_bg_image(path)
