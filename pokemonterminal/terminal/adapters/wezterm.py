import os
import pathlib
from typing import Union

from luaparser import ast, astnodes

from . import TerminalProvider as _TProv


class WezTermTerminalProvider(_TProv):
    @staticmethod
    def __get_config_file():
        # loosely follow the logic detailed at https://wezfurlong.org/wezterm/config/files.html#configuration-files

        # can't check for the command line argument so start by looking at the
        # environment variable
        if (path := os.environ.get('WEZTERM_CONFIG_FILE', None)) is not None:
            return pathlib.Path(path)
        elif (path := os.environ.get('XDG_CONFIG_HOME', None)) is not None:
            return pathlib.Path(path) / 'wezterm' / 'wezterm.lua'
        else:
            return pathlib.Path(os.path.expanduser('~/.wezterm.lua'))

    @staticmethod
    def __set_bg_image(new: Union[os.PathLike[str], str]):
        with open(WezTermTerminalProvider.__get_config_file(), 'r+') as cfg:
            tree = ast.parse(cfg.read())
            dirty = False
            for node in ast.walk(tree):
                if isinstance(node, astnodes.Return):

                    # if the new path is empty then we can remove the node from
                    # the tree entirely
                    if new == '':
                        node.values[0].fields = list(filter(
                            lambda f: f.key.id != 'window_background_image',
                            node.values[0].fields
                        ))
                        dirty = True
                        break

                    # if the node already exists then modify it
                    if len(list(filter(
                            lambda f: f.key.id == 'window_background_image',
                            node.values[0].fields))) > 0:

                        for field in node.values[0].fields:
                            if field.key.id == 'window_background_image' and \
                                    field.value.s != new:
                                field.value = astnodes.String(
                                    str(new), field.value.delimiter
                                )
                                dirty = True
                    else:  # otherwise we will append it to the nodes
                        node.values[0].fields.append(astnodes.Field(
                            astnodes.Name('window_background_image'),
                            astnodes.String(str(new))
                        ))
                        dirty = True
            # technically there's no code path here that doesn't result in dirty
            # being true, but whatever this is ✨ good practice ✨
            # ... not, of course, that the rest of this code is a paragon of
            # good practice bc it doesn't look for other more complicated
            # locations of wezterm config files and also doesn't handle anything
            # other than the simple case of a single return node. meh this isn't
            # for public consumption.
            if dirty:
                cfg.seek(0)
                cfg.truncate()
                cfg.write(ast.to_lua_source(tree))

    @staticmethod
    def is_compatible() -> bool:
        return 'WezTerm' in os.environ.get('TERM_PROGRAM', '')

    @staticmethod
    def clear():
        WezTermTerminalProvider.__set_bg_image('')

    @staticmethod
    def change_terminal(path: str):
        WezTermTerminalProvider.__set_bg_image(path)
