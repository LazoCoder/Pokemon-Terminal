import sys

from .adapters import NamedEvent

def create_named_event(name: str) -> NamedEvent:
    if sys.platform == 'win32':
        from .adapters.win import WindowsNamedEvent
        return WindowsNamedEvent(name)
    else:
        from .adapters.posix import PosixNamedEvent
