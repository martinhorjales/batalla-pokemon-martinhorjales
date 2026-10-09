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

@app.route("/identificacion")
def identificarse():
    return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)


#@app.route("/identificacion", methods=["GET",POST"])
#def identificarse():
#    if request.method == "GET":
#       return render_template("pagina-ingresar-nombre.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)
#    else if request.method == "POST":
#       trainer = request.form["trainer"]
#       return redirect("/pokemons",trainer=trainer)       


@app.route("/pokemons")
def listadoPokemons():
    return render_template("pokemons.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)


@app.route("/pokemons/ID/<int:id>")
def listarPokemon(id):

    pokemon_seleccionado = next((p for p in DATOS if p.get("id") == id), None)

    return render_template("pokemon.html", pokemon=pokemon_seleccionado , DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)


@app.route("/batalla-pokemon")
def combatir():
    return render_template("batalla-pokemon.html", DATOS=DATOS, nombre_proyecto=nombre_proyecto, nombre=nombre, año=año)




if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080")
