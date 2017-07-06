from argparse import Action
from database import Database, Pokemon


class Filter(Action):
    POKEMON_LIST = Database().get_all()
    filtered_list = [p for p in POKEMON_LIST]
    FILTERS = []

    def matches(self, pokemon, value):
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        Filter.FILTERS.append(cls)

    def __call__(self, parser, namespace, value, option_string=None):
        Filter.filtered_list = [pkmn for pkmn in Filter.filtered_list
                                if self.matches(pkmn, value)]


class NameFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return value in pokemon.get_name()


class RegionFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return pokemon.get_region() == value


class LightFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return pokemon.get_dark_threshold() > value


class DarkFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return pokemon.get_dark_threshold() < value


class TypeFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return value in (pokemon.get_pkmn_type(),
                         pokemon.get_pkmn_type_secondary())


class NonExtrasFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return not pokemon.is_extra()


class ExtrasFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return pokemon.is_extra()