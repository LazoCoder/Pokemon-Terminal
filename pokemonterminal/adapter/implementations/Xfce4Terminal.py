import os
import time
import subprocess

from pokemonterminal.adapter.base import TerminalAdapterInterface
from shutil import copyfile
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

class Xfce4Terminal(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        #Get the name of the current terminal
        cmd='ps -o comm= -p "$(($(ps -o ppid= -p "$(($(ps -o sid= -p "$$")))")))"'
        name=subprocess.check_output(cmd, shell=True)
        return b"xfce4" in name

    def set_image_file_path(self, image_file_path):
        cmd="/home/simon/Pictures/terminalBackground/image.jpg"
        copyfile(image_file_path, cmd)
        os.system("./xfce4TerminalChangeBackground.sh '" + image_file_path + "'")

    def clear(self):
        os.system("tybg")
