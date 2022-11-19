from flask import render_template, request

from criptoapp import app
from .models import CriptoModel
from .forms import CryptoForm


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "GET":
        formulario = CryptoForm()
        return render_template("inicio.html", form=formulario)

    else:
        formulario = CryptoForm(data=request.form)
        moneda1 = formulario.moneda1.data
        moneda2 = formulario.moneda2.data
        cantidad = formulario.cantidad.data

        criptomodel = CriptoModel(moneda1, moneda2)
        cambio = criptomodel.consultar_cambio()
        cambio = float(round(cambio, 10))
        cantidad = float(round(cantidad, 10))
        total = cambio*cantidad

        if formulario.consultarapi.data:

            return render_template("inicio.html", form=formulario, numero=total, calculo=cambio)



@app.route("/otra")
def otra():
    return "Otra página"
