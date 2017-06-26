# Used for creating, running and analyzing applescript and bash scripts.

import os
import sys
import subprocess

from adapter import identify

osa_script_fmt = """tell application "System Events"
\ttell current desktop
\t\tset picture to "{}"
\tend tell
end tell"""


def clear_terminal():
    adapter = identify()
    adapter.clear()


def change_terminal(pokemon):
    adapter = identify()
    adapter.set_pokemon(pokemon)


def __run_osascript(stream):
    p = subprocess.Popen(['osascript'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(stream)
    p.communicate()
    p.stdin.close()


def change_wallpaper(pokemon):
    if sys.platform == "darwin":
        script = osa_script_fmt.format(pokemon.get_path())
        __run_osascript(str.encode(script))
    elif sys.platform == "linux":
        os.system(__linux_create_wallpaper_script(pokemon))


def __linux_create_wallpaper_script(pokemon):
    # If its gnome... aka GDMSESSION=gnome-xorg, etc.
    if "gnome" in os.environ.get("GDMSESSION"):
        fmt = 'gsettings set org.gnome.desktop.background picture-uri "file://{}"'
        return fmt.format(pokemon.get_path())
    
    if "xubuntu" in os.environ.get("GDMSESSION"):
      fmt = """for i in $(xfconf-query -c xfce4-desktop -p /backdrop -l|egrep -e "screen.*/monitor.*image-path$" -e "screen.*/monitor.*/last-image$"); do
          xfconf-query -c xfce4-desktop -p $i -n -t string -s "{0}"
          xfconf-query -c xfce4-desktop -p $i -s "{0}"
      done
      """
      return fmt.format(pokemon.get_path())
    elif "lxde" in os.environ.get("GDMSESSION").lower():
        fmt = 'pcmanfm --set-wallpaper="{}"'
        return fmt.format(pokemon.get_path())
    #elif condition of KDE...
    else:
        print("Window manager not supported ")
        exit(1)
