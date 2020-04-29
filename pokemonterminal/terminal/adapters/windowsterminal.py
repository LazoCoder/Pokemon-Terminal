import json
import os
import re

from . import TerminalProvider as _TProv

class WindowsTerminalProvider(_TProv):

    def set_background_image(path: str):
        profiles_path = os.environ['LOCALAPPDATA'] + '\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState\\settings.json'
        with open(profiles_path, 'r+') as json_file:
            # read profiles.json
            # remove comments from json to load
            data = json.loads(WindowsTerminalProvider.comment_remover(json_file.read()))

            # update current profile
            current_profile = os.environ['WT_PROFILE_ID']
            profiles = data['profiles']
            for profile in profiles:
                if (profile['guid'] == current_profile):
                    if (path is None):
                        del profile['backgroundImage']
                    else:
                        profile['backgroundImage'] = path
                    break

            # write to file
            # it lost orignal indent, comment, ...
            json_file.seek(0)
            json.dump(data, json_file, indent=4)
            json_file.truncate()

    def comment_remover(text: str) -> str:
        def replacer(match: re.Match):
            s = match.group(0)
            if s.startswith('/'):
                return " " # note: a space and not an empty string
            else:
                return s
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        return re.sub(pattern, replacer, text)

    def is_compatible() -> bool:
        return "WT_SESSION" in os.environ

    def change_terminal(path: str):
        WindowsTerminalProvider.set_background_image(path)

    def clear():
        WindowsTerminalProvider.set_background_image(None)

    def __str__():
        return "Windows Terminal"