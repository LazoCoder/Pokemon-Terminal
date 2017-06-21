from adapter.implementations.ITerm import ITerm
from adapter.implementations.NullAdapter import NullAdapter
from adapter.implementations.Terminology import Terminology
from adapter.implementations.Tilix import Tilix

available_terminals = [
    Terminology,
    Tilix,
    ITerm
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
