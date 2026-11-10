import random

from flask import Blueprint, redirect, render_template, request, session, url_for

from app.deps import POKEMON_REPOSITORY

pokemon_bp = Blueprint("pokemon", __name__)

@pokemon_bp.route("/pokemons", methods=["GET", "POST"])
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

            for p in POKEMON_REPOSITORY.obtener_pokemons(id):

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
            for p in POKEMON_REPOSITORY.obtener_pokemons(id):
                if (p.get("name") == pokemon.lower() or (pokemon.isdigit() and p.get("id") == int(pokemon))):
                    session["pokemon"] = p
                    return redirect(url_for('combatir'))

            return render_template("pokemons.html", DATOS=POKEMON_REPOSITORY.obtener_pokemons(id), pokemonPermitido=False)

    if request.method == "GET":
        if (trainer == None):
            return render_template("error-pokemons.html", DATOS=POKEMON_REPOSITORY.obtener_pokemons(id))

    return render_template("pokemons.html", DATOS=POKEMON_REPOSITORY.obtener_pokemons(id), pokemonPermitido=True)


@pokemon_bp.route("/pokemons/ID/<int:id>")
def listarPokemon(id):

    pokemon_seleccionado = POKEMON_REPOSITORY.obtener_pokemon_por_id(id)

    if (pokemon_seleccionado == None):
        return render_template("error-pokemon.html")

    return render_template("pokemon.html", pokemon=pokemon_seleccionado)


@pokemon_bp.route("/batalla-pokemon", methods=["GET"])
def combatir():
    pokemon = session.get("pokemon")

    if (not pokemon):
        return render_template("error-sesion.html")

    listaPokemons = POKEMON_REPOSITORY.obtener_nombre_pokemons()

    if (len(pokemon) != 2):
        listaPokemons.remove(pokemon.get("name"))

    pokemonRival = random.choice(listaPokemons)

    ataquesRandom = random.sample(range(0, 9), 4)

    if len(session.get('pokemon')) != 2:
        session["pokemon"] = [pokemon, ataquesRandom]

    for p in POKEMON_REPOSITORY.obtener_pokemons(id):
        if (p.get("name") == pokemonRival):
            pokemonRival = p

    if not session.get('pokemonRival'):
        session["pokemonRival"] = pokemonRival

    return render_template("batalla-pokemon.html", DATOS=POKEMON_REPOSITORY.obtener_pokemons(id))