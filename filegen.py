# The logic for creating the necessary AppleScript to change the background.
# As well as the run.sh to execute the AppleScript.

import os


def get_region(pokemon_number):
    # Determine which region a Pokemon is from.
    if pokemon_number < 1:
        raise Exception("Pokemon number must be at least 1.")
    if pokemon_number < 152:
        return "Generation I - Kanto"
    elif pokemon_number < 252:
        return "Generation II - Johto"
    elif pokemon_number < 387:
        return "Generation III - Hoenn"
    elif pokemon_number < 494:
        return "Generation IV - Sinnoh"
    else:
        raise Exception("Pokemon number must be less than 494.")


def get_filename(pokemon_number):
    # Append zeros at the front if necessary and add the extension.
    # Example: 5 would become 005.png.
    if pokemon_number < 1:
        raise Exception("Pokemon number must be at least 1.")
    elif pokemon_number < 10:
        return "00" + str(pokemon_number) + ".png"
    elif pokemon_number < 100:
        return "0" + str(pokemon_number) + ".png"
    elif pokemon_number < 494:
        return str(pokemon_number) + ".png"
    else:
        raise Exception("Pokemon number must be less than 494.")


def create_applescript_content(region, filename):
    # Create the script that will change the terminal background image.
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"" + os.get_exec_path()[0] + "/Images/" + region + "/" + filename + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def create_applescript(pokemon_number, content=""):
    # Create and save the script for changing the terminal background image.

    if content == "":
        filename = get_filename(pokemon_number)
        region = get_region(pokemon_number)
        content = create_applescript_content(region, filename)

    file = open(os.get_exec_path()[0] + "/Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))
    file.close()


def create_bash_run():
    # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
    content = "#!/bin/bash\n" + "osascript " + os.get_exec_path()[0] + "/Scripts/background.scpt"
    if open(os.get_exec_path()[0] + "/Scripts/run.sh", 'r').read() == content:
        return
    file = open(os.get_exec_path()[0] + "/Scripts/run.sh", 'wb')
    file.write(bytes(content, 'UTF-8'))
    file.close()
