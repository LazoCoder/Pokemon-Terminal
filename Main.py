import os
from sys import argv

# Determine which region a Pokemon is from.
def get_region(pokemon_number):
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


# Append zeros at the front if neccessary and add the extension.
# Example: 5 would become 005.png.
def get_filename(pokemon_number):
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


# Create the script that will change the terminal background image.
def create_script_content(region, filename):
    content = "tell application \"iTerm\"\n"
    content += "\ttell current session of current window\n"
    content += "\t\tset background image to \"" + os.getcwd() + "/Images/" + region + "/" + filename + "\"\n"
    content += "\tend tell\n"
    content += "end tell"
    return content


def create_script(pokemon_number):
    region = get_region(pokemon_number)
    filename = get_filename(pokemon_number)
    content = create_script_content(region, filename)
    file = open("Scripts/background.scpt", "wb")
    file.write(bytes(content, 'UTF-8'))

create_script(int(argv[1]))
os.system('Scripts/run.sh')
