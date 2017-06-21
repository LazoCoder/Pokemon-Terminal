import os

from adapter.base import TerminalAdapterInterface


# todo: broken probably
# do we really need to use applescript? would be nice to
# find a way to do this without.
cwd = os.path.dirname(os.path.realpath(__file__))


class ITerm(TerminalAdapterInterface):
    def __terminal_script(self, path):
        # Create the content for script that will change the terminal background image.
        content = "tell application \"iTerm\"\n"
        content += "\ttell current session of current window\n"
        content += "\t\tset background image to \"" + path + "\"\n"
        content += "\tend tell\n"
        content += "end tell"
        return content

    def __iterm2_clear_script(self):
        # Create and save the script for clearing the terminal background image.
        content = self.__terminal_script("")
        file = open(cwd + "/./Scripts/background.scpt", "wb")
        file.write(bytes(content, 'UTF-8'))
        file.close()

    def __darwin_create_terminal_bash(self):
        # Create and save the run.sh that will execute the AppleScript if the correct run.sh doesn't already exist.
        content = "#!/bin/bash\n" + "osascript " + cwd + "/./Scripts/background.scpt"
        if open(cwd + "/./Scripts/run.sh", 'r').read() == content:
            return
        file = open(cwd + "/./Scripts/run.sh", 'wb')
        file.write(bytes(content, 'UTF-8'))
        file.close()

    def __iterm2_create_terminal_script(self, pokemon):
        # Create and save the script for changing the terminal background image.
        content = self.__terminal_script(pokemon.get_path())
        file = open(cwd + "/./Scripts/background.scpt", "wb")
        file.write(bytes(content, 'UTF-8'))
        file.close()

    def clear(self):
        self.__iterm2_clear_script()
        self.__darwin_create_terminal_bash()
        os.system(cwd + "/./Scripts/run.sh")

    def set_pokemon(self, pokemon):
        # Create, save and run the bash script to change the terminal background.
        self.__iterm2_create_terminal_script(pokemon)
        self.__darwin_create_terminal_bash()
        os.system(cwd + "/./Scripts/run.sh")
