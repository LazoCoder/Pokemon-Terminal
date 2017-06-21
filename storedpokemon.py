class StoredPokemon:

    def __init__(self, name="MissingNo"):
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name
