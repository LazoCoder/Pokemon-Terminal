import os

from pokemonterminal.adapter.base import TerminalAdapterInterface
from shutil import copyfile
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import time
import subprocess

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
       with open(file_path) as old_file:
          for line in old_file:
             new_file.write(line.replace(pattern, subst))
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

class Xfce4Term(TerminalAdapterInterface):
    @staticmethod
    def is_available():
        cmd='ps -o comm= -p "$(($(ps -o ppid= -p "$(($(ps -o sid= -p "$$")))")))"'
        name=subprocess.check_output(cmd, shell=True)
        print(b"xfce4" in name)
        return b"xfce4" in name



    def set_image_file_path(self, image_file_path):
        cmd="/home/simon/Pictures/terminalBackground/image.jpg"
        path="/home/simon/.config/xfce4/terminal/terminalrc"
        copyfile(image_file_path, cmd)
        cmd2="sed -i 's/image.jpg/image1.jpg/g' " + path
        cmd3="sed -i 's/image1.jpg/image.jpg/g' " + path
        os.system("/home/simon/.config/xfce4/terminal/./changebackground.sh")


    def clear(self):
        os.system("tybg")

