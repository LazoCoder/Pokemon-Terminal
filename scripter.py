# Used for creating, running and analyzing applescript and bash scripts.

import os
import sys
import subprocess

from adapter import identify


def clear_terminal():
    adapter = identify()
    adapter.clear()


def change_terminal(pokemon):
    adapter = identify()
    adapter.set_pokemon(pokemon)


def __wallpaper_script(pokemon):
    # Create the content for the script that will change the wallpaper.
    content = "tell application \"System Events\"\n"
    content += "\ttell current desktop\n"
    content += "\t\tset picture to \"" + pokemon.get_path() + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __run_osascript(stream):
    p = subprocess.Popen(['osascript'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(stream)
    p.communicate()
    p.stdin.close()


def change_wallpaper(pokemon):
    if sys.platform == "darwin":
        script = __wallpaper_script(pokemon)
        __run_osascript(str.encode(script))
    if sys.platform == "linux":
        os.system(__linux_create_wallpaper_script(pokemon))


def __linux_create_wallpaper_script(pokemon):
    # If its gnome... aka GDMSESSION=gnome-xorg, etc.
    if os.environ.get("GDMSESSION").find("gnome") >= 0:
        return "gsettings set org.gnome.desktop.background picture-uri " + \
            "\"file://"+ pokemon.get_path()+"\""
    #elif condition of KDE...
    else:
        print("Window manager not supported ")
        exit(1)
