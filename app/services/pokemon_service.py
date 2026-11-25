
class PokemonService:

    def __init__(self,repo):
        self.repo = repo

    def validar_nombre_trainer(self,name):
        if (len(name) >= 3 and len(name) <= 15):
            return True
        else:
            return False

    def devolver_pokemons(self):
        return self.repo.obtener_pokemons()

    def devolver_nombre_pokemons(self):
        return self.repo.obtener_nombre_pokemons()

    def devolver_pokemon_por_id(self,id):
        return self.repo.obtener_pokemon_por_id(id)

    def devolver_pokemons_min_height(self,min_height):
        return self.repo.obtener_pokemons_min_height(min_height)

    def devolver_pokemons_max_weight(self, max_weight):
        return self.repo.obtener_pokemons_max_weight(max_weight)

    def devolver_pokemons_por_tipo(self, tipo):
        return self.repo.obtener_pokemons_por_tipo(tipo)