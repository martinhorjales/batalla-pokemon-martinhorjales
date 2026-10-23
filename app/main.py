from datetime import date
from pathlib import Path
import random

from flask import Flask, json, jsonify, redirect, render_template, request, url_for, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"   # Guardar en ficheros
app.config["SESSION_PERMANENT"] = False     # Sesiones temporales
app.config["SESSION_FILE_DIR"] = "./.flask_session"  # Carpeta donde se guardan
app.secret_key = "clave_super_secreta_martin"

Session(app)

# La ruta se calcula desde este fichero, no desde donde se lance el programa
RUTA_DATOS = Path(__file__).resolve().parent.parent / \
    "data" / "pokemons-starters.json"

# Leemos el JSON una sola vez, al iniciar la aplicación
with RUTA_DATOS.open(encoding="utf-8") as f:
    DATOS = json.load(f)


@app.route("/")
def paginaInicio():
    return render_template("pagina-principal.html")


@app.route("/identificacion", methods=["GET", "POST"])
def identificarse():
    if request.method == "GET":
        return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombrePermitido=True)
    elif request.method == "POST":
        trainer = request.form["trainer"]
        if (len(trainer) >= 3 and len(trainer) <= 15):
            session["trainer"] = trainer
            return redirect(url_for('listadoPokemons'))
        else:
            return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombrePermitido=False)


@app.route("/pokemons", methods=["GET", "POST"])
def listadoPokemons():
    trainer = session.get("trainer")

    if request.method == "POST":
        pokemon = request.form.get("pokemon", "")

        if pokemon == "":
            tipo = request.form.get("pokemon-type-filter", "").lower()
            min_height = request.form.get("min-height-filter", "")
            max_weight = request.form.get("max-weight-filter", "")

            minh = float(min_height) if min_height else None
            maxw = float(max_weight) if max_weight else None

            pokemons_filtrados = []

            for p in DATOS:

                if tipo and tipo.lower() not in p.get("types", []):
                    continue

                altura_m = p.get("height", 0) / 10
                if minh is not None and altura_m < minh:
                    continue

                peso_kg = p.get("weight", 0) / 10
                if maxw is not None and peso_kg > maxw:
                    continue

                pokemons_filtrados.append(p)

            return render_template("pokemons.html", DATOS=pokemons_filtrados, pokemonPermitido=True)

        else:
            for p in DATOS:
                if (p.get("name") == pokemon.lower() or (pokemon.isdigit() and p.get("id") == int(pokemon))):
                    session["pokemon"] = p
                    return redirect(url_for('combatir'))

            return render_template("pokemons.html", DATOS=DATOS, pokemonPermitido=False)

    if request.method == "GET":
        if (trainer == None):
            return render_template("error-pokemons.html", DATOS=DATOS)

    return render_template("pokemons.html", DATOS=DATOS, pokemonPermitido=True)


@app.route("/pokemons/ID/<int:id>")
def listarPokemon(id):

    pokemon_seleccionado = next((p for p in DATOS if p.get("id") == id), None)

    if (pokemon_seleccionado == None):
        return render_template("error-pokemon.html")

    return render_template("pokemon.html", pokemon=pokemon_seleccionado)


@app.route("/batalla-pokemon", methods=["GET"])
def combatir():
    pokemon = session.get("pokemon")

    listaPokemons = ["pikachu", "bulbasaur", "charmander",
                     "squirtle", "eevee", "rowlet", "tepig", "mudkip"]

    if (len(pokemon) != 2):
        listaPokemons.remove(pokemon.get("name"))

    pokemonRival = random.choice(listaPokemons)

    ataquesRandom = random.sample(range(0, 9), 4)

    if len(session.get('pokemon')) != 2:
        session["pokemon"] = [pokemon, ataquesRandom]

    for p in DATOS:
        if (p.get("name") == pokemonRival):
            pokemonRival = p

    if not session.get('pokemonRival'):
        session["pokemonRival"] = pokemonRival

    return render_template("batalla-pokemon.html", DATOS=DATOS)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080", debug=True)
