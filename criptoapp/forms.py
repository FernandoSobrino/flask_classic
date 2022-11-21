from datetime import date, datetime
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, TimeField, IntegerField
from wtforms.validators import DataRequired

from .settings import MONEDAS

class CryptoForm(FlaskForm):

    fecha = DateField('Fecha')
    hora = TimeField('Hora')
    moneda_origen = SelectField('De: ', choices=MONEDAS, validators=[DataRequired(message="Selecciona moneda inicial")])
    moneda_destino = SelectField('A: ', choices=MONEDAS, validators=[DataRequired(message="Selecciona moneda inicial")])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(message="Debes indicar una cantidad")])
    consultarapi = SubmitField("Consultar API")
    borrar = SubmitField("Borrar")
    guardar = SubmitField("Guardar")
    textoapi = StringField()