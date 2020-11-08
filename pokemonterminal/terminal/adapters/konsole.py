import os
from subprocess import run

from . import TerminalProvider as _TProv


class KonsoleProvider(_TProv):
    __colorscheme_path__ = os.environ.get("HOME") + "/.local/share/konsole/"
    __base_colorscheme__ = "Pokemon"

    def is_compatible() -> bool:
        # This gives a false positive if Konsole is open but not the active terminal emulator.
        return "KONSOLE_VERSION" in os.environ

    def change_terminal(path: str):
        # Make it easy to rm
        prefix = "p--"

        pokemon = prefix + path.split("/")[-1].split(".")[0]
        new_scheme_path = (
            KonsoleProvider.__colorscheme_path__ + pokemon + ".colorscheme"
        )

        # The file doesn't need to be read or written if the colorscheme is cached. It saves some disk writes.
        if (
            not os.path.isfile(new_scheme_path)
            or os.stat(
                KonsoleProvider.__colorscheme_path__
                + KonsoleProvider.__base_colorscheme__
                + ".colorscheme",
                follow_symlinks=True,
            ).st_mtime
            > os.stat(new_scheme_path).st_mtime
        ):
            new_scheme = ""
            with open(
                KonsoleProvider.__colorscheme_path__
                + KonsoleProvider.__base_colorscheme__
                + ".colorscheme",
                "r",
            ) as f:
                for line in f:
                    if line.startswith("Wallpaper"):
                        line = "Wallpaper=" + path + "\n"
                    elif line.startswith("Description"):
                        line = "Description=" + pokemon + "\n"

                    new_scheme += line

            with open(new_scheme_path, "w") as f:
                f.write(new_scheme)

        run(["konsoleprofile", "ColorScheme=" + pokemon], check=True)

    def clear():
        run(
            ["konsoleprofile", "ColorScheme=" + KonsoleProvider.__base_colorscheme__],
            check=True,
        )

    def __str__():
        return "Konsole"
