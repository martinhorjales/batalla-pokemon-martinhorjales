from datetime import date
from pathlib import Path

from flask import Flask, json, jsonify, redirect, render_template, request, url_for

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


@app.route("/identificacion", methods=["GET", "POST"])
def identificarse():
    if request.method == "GET":
        return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año, nombrePermitido=True)
    elif request.method == "POST":
        trainer = request.form["trainer"]
        if (len(trainer) >= 3 and len(trainer) <= 15):
            return redirect(url_for('listadoPokemons', trainer=trainer))
        else:
            return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año, nombrePermitido=False)


@app.route("/pokemons")
def listadoPokemons():
    trainer = request.args.get('trainer')

    if (trainer == None):
        return render_template("error-pokemons.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)
    
    return render_template("pokemons.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año ,trainer=trainer)


@app.route("/pokemons/ID/<int:id>")
def listarPokemon(id):

    pokemon_seleccionado = next((p for p in DATOS if p.get("id") == id), None)

    if (pokemon_seleccionado == None):
        return render_template("error-pokemon.html",nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)

    return render_template("pokemon.html", pokemon=pokemon_seleccionado, DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)


@app.route("/batalla-pokemon")
def combatir():
    return render_template("batalla-pokemon.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
