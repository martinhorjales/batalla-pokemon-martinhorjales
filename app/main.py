from datetime import date
from pathlib import Path
import random

from flask import Flask, render_template
from flask_session import Session

from app.routes.pokemons_route import pokemon_bp
from app.routes.usuario_routes import usuario_bp

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"   
app.config["SESSION_PERMANENT"] = False     
app.config["SESSION_FILE_DIR"] = "./.flask_session" 
app.config['SECRET_KEY'] = 'clave_secreta_batalla_pokemon'

Session(app)

app.register_blueprint(usuario_bp)
app.register_blueprint(pokemon_bp)

@app.route("/")
def paginaInicio():
    return render_template("pagina-principal.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8080", debug=True)