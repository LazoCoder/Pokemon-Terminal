import os
import importlib
import inspect
from .adapters import WallpaperProvider


def _is_adapter(member) -> bool:
    return (inspect.isclass(member)
            and issubclass(member, WallpaperProvider)
            and member != WallpaperProvider)


def _get_adapter_classes() -> [WallpaperProvider]:
    dirname = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'adapters')
    adapter_classes = []
    for file_name in sorted(os.listdir(dirname)):
        root, ext = os.path.splitext(file_name)
        if ext.lower() == '.py' and not root.startswith('__'):
            module = importlib.import_module(
                '.' + root, 'pokemonterminal.wallpaper.adapters')
            for _, c in inspect.getmembers(module, _is_adapter):
                adapter_classes.append(c)
    return adapter_classes


def get_current_adapters() -> [WallpaperProvider]:
    arr = _get_adapter_classes()
    return [x for x in arr if x.is_compatible()]
