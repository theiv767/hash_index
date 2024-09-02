# ROTAS 

from flask import render_template
from main import app


@app.route("/")
def homepage():
    return render_template("homepage.html")