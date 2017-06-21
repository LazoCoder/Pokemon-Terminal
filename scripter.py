# Used for creating, running and analyzing applescript and bash scripts.

import os
import sys

from adapter import identify

cwd = os.path.dirname(os.path.realpath(__file__))


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


def __darwin_create_wallpaper_script(pokemon):
    # Create and save the script for changing the wallpaper.
    content = __wallpaper_script(pokemon)
    file = open(cwd + "/./Scripts/wallpaper.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


# Create and save the run.sh that will execute the AppleScript if the correct run.sh
# doesn't already exist.
def __darwin_create_wallpaper_bash():
    content = "#!/bin/bash\n" + "osascript " + cwd + "/./Scripts/wallpaper.scpt"
    if open(cwd + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(cwd + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def change_wallpaper(pokemon):
    if sys.platform == "darwin":
        # Create, save and run the bash script to change the wallpaper.
        __darwin_create_wallpaper_script(pokemon)
        __darwin_create_wallpaper_bash()
        os.system(cwd + "/./Scripts/run.sh")
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
