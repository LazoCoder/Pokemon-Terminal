import sys

if sys.platform == 'win32':
    from .named_event.win import WindowsNamedEvent as platform_event
else:
    from .named_event.posix import PosixNamedEvent as platform_event

PlatformNamedEvent = platform_event
