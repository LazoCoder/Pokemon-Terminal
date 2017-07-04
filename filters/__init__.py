from argparse import Action
from database import Database, Pokemon


class Filter(Action):
    POKEMON_LIST = Database().get_all()
    FILTERS = []

    def matches(self, pokemon, value):
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        Filter.FILTERS.append(cls)

    def __call__(self, parser, namespace, value, option_string=None):
        Filter.POKEMON_LIST = [pkmn for pkmn in Filter.POKEMON_LIST
                               if self.matches(pkmn, value)]


class NameFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return pokemon.get_name().find(value) > -1


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
        return pokemon.get_pkmn_type() == value or\
               pokemon.get_pkmn_type_secondary() == value


class ExtrasFilter(Filter):
    def matches(self, pokemon: Pokemon, value):
        return not pokemon.is_extra()
