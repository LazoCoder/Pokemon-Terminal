from adapter.implementations.ITerm import ITerm
from adapter.implementations.NullAdapter import NullAdapter
from adapter.implementations.Terminology import Terminology
from adapter.implementations.Tilix import Tilix
# from adapter.implementations.XFCE4Terminal import XFCE4Terminal
# from adapter.implementations.Terminator import Terminator

available_terminals = [
    Terminology,
    Tilix,
    Terminator,
    # ITerm,
    # XFCE4Terminal,
]


def identify():
    """
    Identify the terminal we are using based on env vars.
    :return: A terminal adapter interface or a NullAdapter.
    :rtype: TerminalAdapterInterface
    """
    for terminal in available_terminals:
        if terminal.is_available():
            return terminal()

    return NullAdapter()
