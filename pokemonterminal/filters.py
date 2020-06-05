from argparse import Action
from pokemonterminal.database import Database, Pokemon


class Filter(Action):
    POKEMON_LIST = Database().get_all()
    filtered_list = [p for p in POKEMON_LIST]
    FILTERS = []
    EXAMPLE_VAL = None

    def matches(self, pokemon, value):
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        Filter.FILTERS.append(cls)

    def __call__(self, parser, namespace, value, option_string=None):
        Filter.filtered_list = [
            pkmn for pkmn in Filter.filtered_list if self.matches(pkmn, value)
        ]


class NameFilter(Filter):
    EXAMPLE_VAL = "bulb"

    def matches(self, pokemon: Pokemon, value: str):
        return value in pokemon.get_name()


class RegionFilter(Filter):
    EXAMPLE_VAL = ["kanto"]

    def matches(self, pokemon: Pokemon, value: list):
        return pokemon.get_region() in value


class LightFilter(Filter):
    EXAMPLE_VAL = 0.7

    def matches(self, pokemon: Pokemon, value: float):
        return pokemon.get_dark_threshold() > value


class DarkFilter(Filter):
    EXAMPLE_VAL = 0.4

    def matches(self, pokemon: Pokemon, value: float):
        return pokemon.get_dark_threshold() < value


class TypeFilter(Filter):
    EXAMPLE_VAL = ["water"]

    def matches(self, pokemon: Pokemon, value: list):
        return (
            pokemon.get_pkmn_type() in value
            or pokemon.get_pkmn_type_secondary() in value
        )


class NonExtrasFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return not pokemon.is_extra()


class ExtrasFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return pokemon.is_extra()
