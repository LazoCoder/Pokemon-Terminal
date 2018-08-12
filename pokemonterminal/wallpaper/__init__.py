import importlib
import inspect
import pathlib

from .adapters import WallpaperProvider


def _is_adapter(member) -> bool:
    return (inspect.isclass(member)
            and issubclass(member, WallpaperProvider)
            and member != WallpaperProvider)


def _get_adapter_classes() -> [WallpaperProvider]:
    """
    This methods reads all the modules in the adapters folder searching for
    all the implementing wallpaper adapter classes
    thanks for/adapted from https://github.com/cclauss/adapter_pattern/
    """
    adapter_dir = pathlib.Path(__file__).resolve().parent / 'adapters'
    for file in adapter_dir.iterdir():
        if file.suffix.lower() == '.py' and not file.name.startswith('__'):
            module = importlib.import_module('.' + file.name.split('.')[0], 'pokemonterminal.wallpaper.adapters')
            for _, c in inspect.getmembers(module, _is_adapter):
                yield c


def get_current_wallpaper_adapters() -> [WallpaperProvider]:
    arr = _get_adapter_classes()
    return [x for x in arr if x.is_compatible()]
