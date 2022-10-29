from flask import render_template

from criptoapp import app
from .models import CriptoModel


@app.route("/")
def home():
    c = CriptoModel("BTC", "EUR", 3)
    datos = c.consultar_cambio()
    moneda_origen = c.moneda_origen
    cantidad_origen = c.cantidad_from
    moneda_destino = c.moneda_destino
    cambio = datos[0]
    cantidad_destino = datos[1]
    

    return render_template("inicio.html",
        camb=cambio, mon_orig=moneda_origen, mon_dest=moneda_destino, c_dest=cantidad_destino, c_origen=cantidad_origen)


@app.route("/otra")
def otra():
    return "Otra página"
