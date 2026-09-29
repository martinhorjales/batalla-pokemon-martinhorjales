from datetime import date

from flask import Flask ,render_template

app = Flask(__name__)

nombre_proyecto= "batalla-pokemon-martinhorjales"
nombre = "Martín Horjales Monteagudo"
año = date.today().year



@app.route("/")
def hello():
    return render_template("bienvenida.html",nombre_proyecto=nombre_proyecto,nombre=nombre,año=año)

if __name__ == "__main__":
    app.run(host= "127.0.0.1", port="8080")
