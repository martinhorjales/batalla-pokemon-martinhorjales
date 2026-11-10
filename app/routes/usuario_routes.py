from flask import Blueprint, redirect, render_template, request, session, url_for

from app.deps import POKEMON_REPOSITORY, POKEMON_SERVICE

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route('/logout')
def logOut():

    session.clear()

    return render_template("pagina-principal.html")


@usuario_bp.route("/identificacion", methods=["GET", "POST"])
def identificarse():
    if request.method == "GET":
        return render_template("pagina-ingresar-nombre.html",DATOS=POKEMON_REPOSITORY.obtener_pokemons() ,nombrePermitido=True)
    elif request.method == "POST":
        trainer = request.form["trainer"]
        if (POKEMON_SERVICE.validar_nombre_trainer(trainer)):
            session["trainer"] = trainer
            return redirect(url_for('listadoPokemons'))
        else:
            return render_template("pagina-ingresar-nombre.html", nombrePermitido=False)