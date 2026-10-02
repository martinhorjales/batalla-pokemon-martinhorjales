from datetime import date
from pathlib import Path

from flask import Flask, json, jsonify, render_template

app = Flask(__name__)

# La ruta se calcula desde este fichero, no desde donde se lance el programa
RUTA_DATOS = Path(__file__).resolve().parent.parent / \
    "data" / "pokemons-starters.json"

# Leemos el JSON una sola vez, al iniciar la aplicación
with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)

nombre_proyecto = "batalla-pokemon-martinhorjales"
nombre = "Martín Horjales Monteagudo"
año = date.today().year


@app.route("/")
def paginaInicio():
    return render_template("pagina-principal.html", nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)


@app.route("/pokemons")
def listadoPokemons():
    return render_template("pokemons.html",DATOS=DATOS)


# @app.route("/pokemons/ID/<integer:id>")
# def listarPokemon():
#     return render_template("pokemon.html",DATOS)


# @app.route("/p")
# def home():
#     return jsonify(DATOS)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
