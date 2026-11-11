from functools import wraps
import random
from flask import Blueprint, redirect, render_template, request, session, url_for
from app.deps import POKEMON_REPOSITORY

pokemon_bp = Blueprint("pokemon", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("trainer"):
            return redirect(url_for('usuario.identificarse'))
        return f(*args, **kwargs)
    return decorated_function

@pokemon_bp.route("/pokemons", methods=["GET", "POST"])
@login_required
def listadoPokemons():
    if request.method == "POST":
        pokemon = request.form.get("pokemon", "")
        
        if pokemon:
            for p in POKEMON_REPOSITORY.carga_datos():
                if (p.get("name") == pokemon.lower() or (pokemon.isdigit() and p.get("id") == int(pokemon))):
                    session["pokemon"] = p
                    return redirect(url_for('pokemon.combatir'))

            return render_template("pokemons.html", DATOS=POKEMON_REPOSITORY.carga_datos(), pokemonPermitido=False)

    tipo = request.args.get("pokemon-type-filter", "").lower()
    min_height = request.args.get("min-height-filter", "")
    max_weight = request.args.get("max-weight-filter", "")

    try:
        minh = float(min_height) if min_height else None
    except ValueError:
        minh = None

    try:
        maxw = float(max_weight) if max_weight else None
    except ValueError:
        maxw = None

    pokemons_filtrados = []

    for p in POKEMON_REPOSITORY.carga_datos():
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


@pokemon_bp.route("/pokemons/ID/<int:id>")
@login_required
def listarPokemon(id):
    pokemon_seleccionado = POKEMON_REPOSITORY.obtener_pokemon_por_id(id)

    if (pokemon_seleccionado == None):
        return render_template("error-pokemon.html")

    return render_template("pokemon.html", pokemon=pokemon_seleccionado)


@pokemon_bp.route("/batalla-pokemon", methods=["GET"])
@login_required
def combatir():
    pokemon_session = session.get("pokemon")

    if not pokemon_session:
        return render_template("error-sesion.html")

    if isinstance(pokemon_session, list) and len(pokemon_session) == 2:
        pokemon_data = pokemon_session[0]
    else:
        pokemon_data = pokemon_session

    listaPokemons = POKEMON_REPOSITORY.obtener_nombre_pokemons()

    nombre_jugador = pokemon_data.get("name")
    if nombre_jugador in listaPokemons:
        listaPokemons.remove(nombre_jugador)

    pokemonRival = random.choice(listaPokemons)
    ataquesRandom = random.sample(range(0, 9), 4)

    if not isinstance(pokemon_session, list) or len(pokemon_session) != 2:
        session["pokemon"] = [pokemon_data, ataquesRandom]

    if not session.get('pokemonRival'):
        for p in POKEMON_REPOSITORY.carga_datos():
            if p.get("name") == pokemonRival:
                session["pokemonRival"] = p
                break

    return render_template("batalla-pokemon.html", DATOS=POKEMON_REPOSITORY.carga_datos())