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


def __run_osascript(stream):
    p = subprocess.Popen(['osascript'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write(stream)
    p.communicate()
    p.stdin.close()

def __linux_create_wallpaper_script(image_file_path):

    desktop_session = os.environ.get("DESKTOP_SESSION", "")
    # just in case is not present, check for XDG_CURRENT_DESKTOP
    if not desktop_session:
        desktop_session = os.environ.get("XDG_CURRENT_DESKTOP", "")

    desktop_session = desktop_session.lower()
        
    if "gnome" in desktop_session:
        fmt = 'gsettings set org.gnome.desktop.background picture-uri "file://{}"'
        return fmt.format(image_file_path)
    elif "xfce" in desktop_session:
      fmt = """for i in $(xfconf-query -c xfce4-desktop -p /backdrop -l|egrep -e "screen.*/monitor.*image-path$" -e "screen.*/monitor.*/last-image$"); do
          xfconf-query -c xfce4-desktop -p $i -n -t string -s "{0}"
          xfconf-query -c xfce4-desktop -p $i -s "{0}"
      done
      """
      return fmt.format(image_file_path)
    elif "lxde" in desktop_session:
        fmt = 'pcmanfm --set-wallpaper="{}"'
        return fmt.format(image_file_path)
    else:
        print("Window manager not supported ")
        exit(1)


def clear_terminal():
    adapter = identify()
    adapter.clear()


def change_terminal(image_file_path):
    if not isinstance(image_file_path, str):
        print("A image path must be passed to the change terminal function.")
        return
    adapter = identify()
    if adapter is None:
        print("Terminal not supported")
    adapter.set_image_file_path(image_file_path)


def change_wallpaper(image_file_path):
    if not isinstance(image_file_path, str):
        print("A image path must be passed to the change wallpapper function.")
        return
    if sys.platform == "darwin":
        script = osa_script_fmt.format(image_file_path)
        __run_osascript(str.encode(script))
    elif sys.platform == "linux":
        os.system(__linux_create_wallpaper_script(image_file_path))
