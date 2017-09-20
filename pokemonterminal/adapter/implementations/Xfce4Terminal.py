import os
import time
import subprocess

from pokemonterminal.adapter.base import TerminalAdapterInterface
from shutil import copyfile
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
from pathlib import Path

class Xfce4Terminal(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        #Get the name of the current terminal
        cmd='ps -o comm= -p "$(($(ps -o ppid= -p "$(($(ps -o sid= -p "$$")))")))"'
        name=subprocess.check_output(cmd, shell=True)
        return b"xfce4" in name

    def set_image_file_path(self, image_file_path):
        xfce4_config_path = str(Path.home()) + "/.config/xfce4/terminal/terminalrc" 

        #read xfce4-terminal config file
        f = open(xfce4_config_path, "r")
        lines = f.readlines()
        f.close()
        f = open(xfce4_config_path, "w")

        #replace the line setting xfce4-terminal's background image
        for line in lines:
            if "BackgroundImage" not in line:
                f.write(line)
            else:
                f.write("BackgroundImageFile=" + image_file_path + "\n")
        f.close()


    def clear(self):
        os.system("tybg")
