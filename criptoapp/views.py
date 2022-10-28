from criptoapp import app
from criptoapp.models import *

@app.route("/")
def home():
    c = CriptoModel("BTC","EUR")
    cambio = c.consultar_cambio()
    moneda_origen = c.moneda_origen
    moneda_destino = c.moneda_destino
    return("Un {} vale {:,.2f} {}".format(moneda_origen,cambio,moneda_destino))

@app.route("/otra")
def otra():
    return "Otra página"