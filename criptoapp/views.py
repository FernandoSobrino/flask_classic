from flask import render_template

from criptoapp import app
from .models import CriptoModel

@app.route("/")
def home():
    c = CriptoModel("BTC","EUR")
    cambio = c.consultar_cambio()
    moneda_origen = c.moneda_origen
    moneda_destino = c.moneda_destino
    return render_template("inicio.html",camb=cambio,mon_orig=moneda_origen,mon_dest=moneda_destino)
    

@app.route("/otra")
def otra():
    return "Otra página"