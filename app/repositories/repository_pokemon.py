from pathlib import Path

from flask import json

from app.models.pokemon import Pokemon


class PokemonRepository:

    def ruta_datos(self):
        ruta = Path(__file__).resolve().parent.parent / \
            "data" / "pokemons-starters.json"
        return ruta

    def carga_datos(self):
        with self.ruta_datos(self).open(encoding="utf-8") as f:
            datos = json.load(f)
        return datos

    def obtener_pokemons(self):
        pokemons = []
        for pokemon in self.carga_datos():
            pokemons.append(Pokemon(**pokemon))
        return pokemons

    def obtener_pokemon_por_id(self, id):
        pokemon = None
        for p in self.carga_datos():
            if (p["id"] == id):
                pokemon = Pokemon(**p)
        return pokemon

    def obtener_pokemons_min_height(self, min_height):
        pokemons_filtados_por_altura = []
        for p in self.carga_datos():
            if (p["height"] >= min_height):
                pokemons_filtados_por_altura.append(Pokemon(**p))
        return pokemons_filtados_por_altura

    def obtener_pokemons_max_weight(self, max_weight):
        pokemons_filtados_por_peso = []
        for p in self.carga_datos():
            if (p["weight"] <= max_weight):
                pokemons_filtados_por_peso.append(Pokemon(**p))
        return pokemons_filtados_por_peso

    def obtener_pokemons_por_tipo(self, tipo):
        pokemons_filtrados_por_tipo = []
        for p in self.carga_datos():
            if (p["types"][0] == tipo or p["types"][1] == tipo):
                pokemons_filtrados_por_tipo.append(Pokemon(**p))
        return pokemons_filtrados_por_tipo
