from . import TerminalProvider as _TProv
import fileinput
import os
import re
import subprocess
import sys

CONF_PATH = os.path.join(os.path.expanduser('~'), '.hyper.js')


class HyperProvider(_TProv):
    def is_compatible() -> bool:
        # if you use WSL you should symlink .hyper.js to the home directory
        return os.path.exists(CONF_PATH)

    def change_terminal(path: str) -> None:
        r = re.compile(r"(css: '\.terms_terms ){( background: url\()(.+)(\) center;.+)}(',)")
        found = False
        with open(CONF_PATH) as conf:
            for line in conf:
                if r.search(line):
                    found = True
                    break

        if not found:  # add css
            for line in fileinput.input(CONF_PATH, inplace=True):
                if r.search(line):
                    line = re.sub(r"css: '',$",
                                  f"\.terms_terms {{ background: url(file://{path}) center; background-size: cover; "
                                  f"}}',", line)
                    sys.stdout.write(re.sub(r"termCSS: ''$", "termCSS: 'x-screen { background: transparent "
                                                             "!important; }',", line))
                    return

        for line in fileinput.input(CONF_PATH, inplace=True):
            line = r.sub(r'\1{{\2"file://{}"\4}}\5'.format(path), line)
            sys.stdout.write(line)

    def clear():
        cmd = 'cls' if sys.platform == 'win32' else 'clear'
        subprocess.call(cmd, shell=True)

    def __str__():
        return "Hyper Terminal"
