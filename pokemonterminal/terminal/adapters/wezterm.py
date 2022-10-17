import os
import pathlib
from typing import Union

from luaparser import ast, astnodes

from . import TerminalProvider as _TProv


class WezTermTerminalProvider(_TProv):
    @staticmethod
    def __set_bg_image(new: Union[os.PathLike, str]):
        with open(pathlib.Path(os.path.expanduser('~/.wezterm.lua')), 'r+') as cfg:
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
                                    new, field.value.delimiter
                                )
                                dirty = True
                    else:  # otherwise we will append it to the nodes
                        node.values[0].fields.append(astnodes.Field(
                            astnodes.Name('window_background_image'),
                            astnodes.String(new)
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

