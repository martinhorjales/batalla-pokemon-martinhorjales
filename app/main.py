from datetime import date
from pathlib import Path
import random

from flask import Flask, json, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

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
            return redirect(url_for('listadoPokemons', trainer=trainer))
        else:
            return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombrePermitido=False)


@app.route("/pokemons", methods=["GET", "POST"])
def listadoPokemons():
    trainer = request.args.get('trainer')

    if request.method == "POST":
        pokemon = request.form.get("pokemon", "")
        trainer = request.form.get('trainer') or trainer

        if pokemon == "":
            tipo = request.form.get("pokemon-type-filter", "")
            min_height = request.form.get("min-height-filter", "")
            max_weight = request.form.get("max-weight-filter", "")

        else:
            for p in DATOS:
                if (p.get("name") == pokemon.lower() or (pokemon.isdigit() and p.get("id") == int(pokemon))):
                    pokemon = p.get("name")
                    return redirect(url_for('combatir', pokemon=pokemon, trainer=trainer))

            return render_template("pokemons.html", DATOS=DATOS, trainer=trainer, pokemonPermitido=False)

    if request.method == "GET":
        if (trainer == None):
            return render_template("error-pokemons.html", DATOS=DATOS, año=año)

    return render_template("pokemons.html", DATOS=DATOS,trainer=trainer, pokemonPermitido=True)


@app.route("/pokemons/ID/<int:id>")
def listarPokemon(id):
    trainer = request.args.get('trainer')

    pokemon_seleccionado = next((p for p in DATOS if p.get("id") == id), None)

    if (pokemon_seleccionado == None):
        return render_template("error-pokemon.html")

    return render_template("pokemon.html", pokemon=pokemon_seleccionado,trainer=trainer)


@app.route("/batalla-pokemon", methods=["GET"])
def combatir():
    trainer = request.args.get('trainer')
    pokemon = request.args.get('pokemon')

    pokemonUsuario = None

    for p in DATOS:
        if (p.get("name") == pokemon):
            pokemonUsuario = p

    listaPokemons = ["pikachu", "bulbasaur", "charmander",
                     "squirtle", "eevee", "rowlet", "tepig", "mudkip"]
    listaPokemons.remove(pokemonUsuario.get("name"))

    pokemonRival = random.choice(listaPokemons)

    ataquesRandom = random.sample(range(0, 9), 4)

    for p in DATOS:
        if (p.get("name") == pokemonRival):
            pokemonRival = p

    return render_template("batalla-pokemon.html", DATOS=DATOS,pokemonUsuario=pokemonUsuario, trainer=trainer, pokemonRival=pokemonRival, ataquesRandom=ataquesRandom)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080", debug=True)
