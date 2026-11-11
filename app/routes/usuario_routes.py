from flask import Blueprint, redirect, render_template, request, session, url_for
from app.deps import POKEMON_REPOSITORY
from app.forms.usuario_form import EntrenadorForm

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route('/logout')
def logOut():
    session.clear()
    return redirect(url_for('paginaInicio'))

@usuario_bp.route("/identificacion", methods=["GET", "POST"])
def identificarse():
    form = EntrenadorForm()
    
    if form.validate_on_submit():
        session["trainer"] = form.trainer.data
        return redirect(url_for('pokemon.listadoPokemons'))
    
    return render_template("pagina-ingresar-nombre.html",DATOS=POKEMON_REPOSITORY.obtener_pokemons() ,form=form)