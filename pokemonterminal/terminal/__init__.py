import importlib
import inspect
import pathlib

from .adapters import TerminalProvider


def _is_adapter(member) -> bool:
    return (
        inspect.isclass(member)
        and issubclass(member, TerminalProvider)
        and member != TerminalProvider
    )


def _get_adapter_classes() -> [TerminalProvider]:
    """
    This methods reads all the modules in the adapters folder searching for
    all the implementing wallpaper adapter classes
    thanks for/adapted from https://github.com/cclauss/adapter_pattern/
    """
    adapter_dir = pathlib.Path(__file__).resolve().parent / "adapters"
    for file in adapter_dir.iterdir():
        if file.suffix.lower() == ".py" and not file.name.startswith("__"):
            module = importlib.import_module(
                "." + file.name.split(".")[0], "pokemonterminal.terminal.adapters"
            )
            for _, c in inspect.getmembers(module, _is_adapter):
                yield c


def get_current_terminal_adapters() -> [TerminalProvider]:
    arr = _get_adapter_classes()
    return [x for x in arr if x.is_compatible()]
