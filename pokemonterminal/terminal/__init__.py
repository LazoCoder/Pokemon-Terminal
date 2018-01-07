import os
import importlib
import inspect
from .adapters import TerminalProvider


def _is_adapter(member) -> bool:
    return (inspect.isclass(member)
            and issubclass(member, TerminalProvider)
            and member != TerminalProvider)


def _get_adapter_classes() -> [TerminalProvider]:
    """
    This methods reads all the modules in the adapters folder searching for
    all the implementing wallpaper adapter classes
    thanks for/adapted from https://github.com/cclauss/adapter_pattern/
    """
    dirname = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'adapters')
    adapter_classes = []
    for file_name in sorted(os.listdir(dirname)):
        root, ext = os.path.splitext(file_name)
        if ext.lower() == '.py' and not root.startswith('__'):
            module = importlib.import_module(
                '.' + root, 'pokemonterminal.terminal.adapters')
            for _, c in inspect.getmembers(module, _is_adapter):
                adapter_classes.append(c)
    return adapter_classes


def get_current_terminal_adapters() -> [TerminalProvider]:
    arr = _get_adapter_classes()
    return [x for x in arr if x.is_compatible()]
