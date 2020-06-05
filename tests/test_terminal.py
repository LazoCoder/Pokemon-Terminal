from pokemonterminal.terminal import _get_adapter_classes
import os.path as __p
import inspect as __inspct


def test_terminal_adapter_classes():
    all_adapter = list(_get_adapter_classes())
    files = {__inspct.getfile(x) for x in all_adapter}
    print("all adapter classes:\n", files)
    assert len(all_adapter) >= len(
        files
    ), "Some of the files in the adapter module don't define an adapter"
    module_name = {
        x.__name__: __p.splitext(__p.basename(__inspct.getfile(x)))[0]
        for x in all_adapter
    }
    print("'class: module' map\n", module_name)
    assert all(
        y.lower() in x.lower() for x, y in module_name.items()
    ), "Some of the adapters are defined in unrelated named modules"
