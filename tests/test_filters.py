from pokemonterminal.filters import Filter
import pytest


def test_basic_loading():
    assert len(Filter.POKEMON_LIST) >= 493
    assert len(Filter.filtered_list) == len(Filter.POKEMON_LIST)


def test_filters_infrastructure():
    inst = Filter(None, None)
    with pytest.raises(NotImplementedError):
        inst.matches(None, None)
    for fltr in Filter.FILTERS:
        fltr = fltr(None, None)
        filtered = [
            pkmn for pkmn in Filter.POKEMON_LIST if fltr.matches(pkmn, fltr.EXAMPLE_VAL)
        ]
        assert len(filtered) < len(Filter.POKEMON_LIST)


if __name__ == "__main__":
    # Test runner: Runs all functions whose name begins with `test_`
    # locals() changes when trying to do this without the list comprehension!!!
    name_funcs = [(n, f) for n, f in locals().items() if n.startswith("test_")]
    for name, func in name_funcs:
        if callable(func):
            func()
        else:
            print(name + " is not callable()!")
