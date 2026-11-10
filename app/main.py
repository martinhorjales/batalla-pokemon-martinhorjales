from datetime import date
from pathlib import Path
import random

from flask import Flask, json, jsonify, redirect, render_template, request, url_for, session
from flask_session import Session

from app.routes.pokemons_route import pokemon_bp
from app.routes.usuario_routes import usuario_bp

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"   # Guardar en ficheros
app.config["SESSION_PERMANENT"] = False     # Sesiones temporales
app.config["SESSION_FILE_DIR"] = "./.flask_session"  # Carpeta donde se guardan
app.secret_key = "clave_super_secreta_martin"

Session(app)

app.register_blueprint(pokemon_bp, url_prefix="/")
app.register_blueprint(usuario_bp, url_prefix="/")


@app.route("/")
def paginaInicio():

    return render_template("pagina-principal.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080", debug=True)
