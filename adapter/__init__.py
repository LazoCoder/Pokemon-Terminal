import os

import sys

from adapter.implementations.ITerm import ITerm
from adapter.implementations.NullAdapter import NullAdapter
from adapter.implementations.Terminology import Terminology
from adapter.implementations.Tilix import Tilix


def identify():
    """
    Identify the terminal we are using based on env vars.
    :return: A terminal adapter interface or a NullAdapter.
    :rtype: TerminalAdapterInterface
    """
    if os.environ.get("TERMINOLOGY") == '1':
        return Terminology()

    if "TILIX_ID" in os.environ:
        return Tilix()

    if os.environ.get("ITERM_PROFILE"):
        return ITerm()

    return NullAdapter()
