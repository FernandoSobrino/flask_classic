from flask import render_template, request, redirect, flash, url_for
from datetime import date, datetime

from criptoapp import app
from .settings import DB_PATH
from .models import CriptoModel, DBManager
from .forms import CryptoForm


@app.route("/", methods=["GET", "POST"])
def home():
    global pulsado

    if request.method == "GET":
        formulario = CryptoForm()
        pulsado = False
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
        total = cambio*cantidad

        if formulario.consultarapi.data:
            pulsado = True
            return render_template("inicio.html", form=formulario, numero=total, calculo=cambio)

        if formulario.enviar.data:
            if pulsado == True:
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
                    params = (fecha, hora, moneda_origen, cantidad, moneda_destino, total)
                    resultado = db.consultaParametros(consulta,params)
                
                if resultado:
                    flash("Movimiento Actualizado Correctamente",category="exito")
                    return redirect(url_for("otra"))

@app.route("/otra")
def otra():
    db = DBManager(DB_PATH)
    resultado  = db.consultaSQL("SELECT * from registros")
    ultimo_movimiento = resultado.pop()
    return f"El movimiento {ultimo_movimiento} se ha cargado correctamente"
