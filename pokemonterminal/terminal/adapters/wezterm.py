import math
import os
import pathlib
from typing import Union

from colorthief import ColorThief
from luaparser import ast, astnodes
from PIL import Image, ImageStat

from . import TerminalProvider as _TProv


class WezTermTerminalProvider(_TProv):
    @staticmethod
    def __get_brightness_for_image(img: pathlib.Path):
        with Image.open(img) as im:
            r, g, b = ImageStat.Stat(im).mean

            return -0.25 * (math.sqrt(0.299 * (r**2) + 0.587 * (g**2) + 0.114 * (b**2)) / 255) + 0.25

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
    def __get_background_table(img):
        r, g, b = ColorThief(img).get_color()
        # HACK: need to specify by index here because we can't have anonymous
        #   fields, i guess
        return astnodes.Table([
            astnodes.Field(astnodes.Name('[1]'), astnodes.Table([
                astnodes.Field(astnodes.Name('source'), astnodes.Table([
                    astnodes.Field(astnodes.Name('Color'),
                                   astnodes.String(f'rgb({r}, {g}, {b})')),
                ])),
                astnodes.Field(astnodes.Name('height'),
                               astnodes.String('100%')),
                astnodes.Field(astnodes.Name('width'),
                               astnodes.String('100%')),
                brightness := astnodes.Field(astnodes.Name('hsb'), astnodes.Table([
                    astnodes.Field(astnodes.Name('brightness'),
                                   astnodes.Number(WezTermTerminalProvider.__get_brightness_for_image(img))),
                ])),
            ])),
            astnodes.Field(astnodes.Name('[2]'), astnodes.Table([
                astnodes.Field(astnodes.Name('source'), astnodes.Table([
                    astnodes.Field(astnodes.Name(
                        'File'), astnodes.String(str(img))),
                ])),
                # automatically adjust brightness based on average perceived
                # brightness of the image
                # see https://stackoverflow.com/questions/3490727/what-are-some-methods-to-analyze-image-brightness-using-python
                brightness,
                astnodes.Field(astnodes.Name(
                    'height'), astnodes.String('Contain')),
                astnodes.Field(astnodes.Name(
                    'repeat_y'), astnodes.String('NoRepeat')),
                astnodes.Field(astnodes.Name('vertical_align'),
                               astnodes.String('Middle')),
            ])),
        ])

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
                            lambda f: f.key.id != 'background',
                            node.values[0].fields
                        ))
                        dirty = True
                        break

                    # if the node already exists then modify it
                    if len(list(filter(
                            lambda f: f.key.id == 'background',
                            node.values[0].fields))) > 0:

                        for field in node.values[0].fields:
                            if field.key.id == 'background':
                                # but only if there's actually a change to be made
                                if len(list(filter(
                                    lambda f: f.key.id == 'source' and f.value.fields[0].value.s == new,
                                    field.value.fields[0].value.fields
                                ))) == 0:

                                    field.value = WezTermTerminalProvider.__get_background_table(
                                        new)
                                    dirty = True
                    else:  # otherwise we will append it to the nodes
                        node.values[0].fields.append(astnodes.Field(
                            astnodes.Name('background'),
                            WezTermTerminalProvider.__get_background_table(new)
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
