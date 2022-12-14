from flask import render_template, request, redirect, flash, url_for
from datetime import date, datetime

from criptoapp import app
from . import DB_PATH
from .models import CriptoModel, DBManager, CriptoSuma
from .forms import CryptoForm


@app.route("/", methods=["GET", "POST"])
def home():
    global boton_consulta_pulsado

    if request.method == "GET":
        formulario = CryptoForm()
        boton_consulta_pulsado = False
        return render_template("inicio.html", form=formulario)

    else:
        formulario = CryptoForm(data=request.form)
        moneda_origen = formulario.moneda_origen.data
        moneda_destino = formulario.moneda_destino.data
        cantidad = formulario.cantidad.data

        criptomodel = CriptoModel(moneda_origen, moneda_destino)
        cambio = criptomodel.consultar_cambio()
        cambio = float(round(cambio, 10))
        cantidad = float(round(cantidad, 10))

        total = cantidad*cambio

        total_formateado = f'{total:.5f}'
        cambio_formateado = f'{cambio:.10f}'

        if formulario.consultarapi.data:
            boton_consulta_pulsado = True
            return render_template("inicio.html", form=formulario, total=total_formateado, cambio=cambio_formateado)

        if formulario.guardar.data:
            if boton_consulta_pulsado == True:
                if formulario.validate():
                    formulario = CryptoForm(data=request.form)
                    db = DBManager(DB_PATH)
                    consulta = "INSERT INTO registros (date,time,moneda_from,cantidad_from,moneda_to,cantidad_to) VALUES(?,?,?,?,?,?)"
                    cantidad = float(formulario.cantidad.data)
                    moneda_origen = str(moneda_origen)
                    moneda_destino = str(moneda_destino)
                    formulario.fecha.data = date.today()
                    fecha = formulario.fecha.data
                    formulario.hora.data = datetime.today().strftime('%H:%M:%S')
                    hora = formulario.hora.data
                    params = (fecha, hora, moneda_origen,
                              cantidad, moneda_destino, total)
                    resultado = db.consultaParametros(consulta, params)

                if resultado:
                    flash("Movimiento Actualizado :)", category="exito")
                    return redirect(url_for("register"))

        if formulario.borrar.data:
            boton_consulta_pulsado = False
            return redirect(url_for("home"))


@app.route("/register")
def register():
    db = DBManager(DB_PATH)
    registros = db.consultaSQL("SELECT * from registros")
    return render_template("registros.html", regs=registros)


@app.route("/status", methods=["GET"])
def status():
    db = DBManager(DB_PATH)
    euro_to = db.consultaResultado(
        "SELECT sum(cantidad_to) FROM registros WHERE moneda_to='EUR'")
    euro_to = euro_to[0]

    euro_from = db.consultaResultado(
        "SELECT sum(cantidad_from) FROM registros WHERE moneda_from='EUR'")
    euro_from = euro_from[0]

    saldo_euros_invertidos = euro_to - euro_from
    saldo_euros_invertidos = round(saldo_euros_invertidos, 8)
    total_euros_invertidos = euro_from

    # total monedas_from convertidas a EUROS
    valor_monedas_from = db.consultaTotales(
        "SELECT moneda_from, sum(cantidad_from) FROM registros GROUP BY moneda_from")
    criptosuma_from = CriptoSuma(valor_monedas_from)

    # total monedas_to convertidas a EUROS
    valor_monedas_to = db.consultaTotales(
        "SELECT moneda_to, sum(cantidad_to) FROM registros GROUP BY moneda_to")
    criptosuma_to = CriptoSuma(valor_monedas_to)

    inversion_atrapada = criptosuma_to.sumar_monedas() - criptosuma_from.sumar_monedas()
    valor_actual = total_euros_invertidos + saldo_euros_invertidos + inversion_atrapada
    valor_actual = round(valor_actual, 8)
    return render_template(
        "status.html", total_euros_invertidos=total_euros_invertidos, valor_actual=valor_actual)
