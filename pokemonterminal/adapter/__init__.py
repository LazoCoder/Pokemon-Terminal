from pokemonterminal.adapter.implementations.ITerm import ITerm
from pokemonterminal.adapter.implementations.NullAdapter import NullAdapter
from pokemonterminal.adapter.implementations.Terminology import Terminology
from pokemonterminal.adapter.implementations.Tilix import Tilix
from pokemonterminal.adapter.implementations.Xfce4Terminal import Xfce4Term



available_terminals = [
    Terminology,
    Tilix,
    ITerm,
    Xfce4Term
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
