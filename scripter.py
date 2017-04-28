# Used for creating and running applescript and bash scripts.

import os


def __terminal_script(pokemon):
    # Create the content for script that will change the terminal background image.
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"" + pokemon.get_path() + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __wallpaper_script(pokemon):
    # Create the content for the script that will change the wallpaper.
    content = "tell application \"System Events\"\n"
    content += "\ttell current desktop\n"
    content += "\t\tset picture to \"" + pokemon.get_path() + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def __create_terminal_script(pokemon):
    # Create and save the script for changing the terminal background image.
    content = __terminal_script(pokemon)
    file = open(os.get_exec_path()[0] + "/./Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_wallpaper_script(pokemon):
    # Create and save the script for changing the wallpaper.
    content = __wallpaper_script(pokemon)
    file = open(os.get_exec_path()[0] + "/./Scripts/wallpaper.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_terminal_bash():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + os.get_exec_path()[0] + "/./Scripts/background.scpt"
    if open(os.get_exec_path()[0] + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(os.get_exec_path()[0] + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def __create_wallpaper_bash():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + os.get_exec_path()[0] + "/./Scripts/wallpaper.scpt"
    if open(os.get_exec_path()[0] + "/./Scripts/run.sh", 'r').read() == content:
        return
    file = open(os.get_exec_path()[0] + "/./Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()


def change_terminal(pokemon):
    # Create, save and run the bash script to change the terminal background.
    __create_terminal_script(pokemon)
    __create_terminal_bash()
    os.system(os.get_exec_path()[0] + "/./Scripts/run.sh")


def change_wallpaper(pokemon):
    # Create, save and run the bash script to change the wallpaper.
    __create_wallpaper_script(pokemon)
    __create_wallpaper_bash()
    os.system(os.get_exec_path()[0] + "/./Scripts/run.sh")
