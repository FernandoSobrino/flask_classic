import sqlite3
import requests

from .settings import APIKEY


class DBManager:
    def __init__(self, ruta):
        self.ruta = ruta

    def consultaSQL(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)

        self.registros = []
        nombres_columnas = []

        for desc_columna in cursor.description:
            nombres_columnas.append(desc_columna[0])

        datos = cursor.fetchall()
        for dato in datos:
            registro = {}
            indice = 0
            for nombre in nombres_columnas:
                registro[nombre] = dato[indice]
                indice += 1
            self.registros.append(registro)
        conexion.close()

        return self.registros

    def consultaParametros(self, consulta, params):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        resultado = False
        try:
            cursor.execute(consulta, params)
            conexion.commit()
            resultado = True
        except Exception as error:
            print("ERROR EN LA BBDD", error)
            conexion.rollback()
        conexion.close()
        return resultado

    def consultaResultado(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        datos = cursor.fetchone()
        conexion.commit()
        conexion.close()
        return datos

    def consultaTotales(self, consulta):
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        datos = cursor.fetchall()
        conexion.commit()
        conexion.close()
        return datos

    def eliminarRegistros(self):
        "Método de prueba para eliminar los registros"
        consulta = "DELETE from registros"
        conexion = sqlite3.connect(self.ruta)
        cursor = conexion.cursor()
        cursor.execute(consulta)
        conexion.commit()
        conexion.close()


class APIError(Exception):
    # Definición de una clase para "elevar" una excepción a medida para la consulta a la API
    pass


class CriptoModel:
    """
    - Moneda Origen
    - Moneda Destino
    - Tipo de cambio
    - Consultar cambio (método)
    """

    def __init__(self, origen, destino):
        """
        Construye un objeto con las monedas origen y destino y
        el cambio obtenido desde CoinAPI inicializado a cero
        """
        self.moneda_origen = origen
        self.moneda_destino = destino
        self.cambio = 0.0

    def consultar_cambio(self):
        """
        Consulta el cambio entre la moneda origen y la moneda destino
        utilizando la API REST CoinAPI
        """
        cabeceras = {"X-CoinAPI-Key": APIKEY}

        url = f"http://rest.coinapi.io/v1/exchangerate/{self.moneda_origen}/{self.moneda_destino}"
        respuesta = requests.get(url, headers=cabeceras)

        if respuesta.status_code == 200:
            # guardo el cambio obtenido
            self.cambio = respuesta.json()["rate"]
            return self.cambio

        else:
            raise APIError(
                "Ha ocurrido un error {} {} al consultar la API".format(
                    respuesta.status_code, respuesta.reason
                )
            )


class CriptoSuma:
    def __init__(self,consultaSQL):
        self.consulta = consultaSQL

    def sumar_monedas(self):
        valor_monedas = self.consulta
        totales_monedas = []
        for valor in valor_monedas:
            cripto = CriptoModel(valor[0], "EUR")
            if valor[0] == "EUR":
                continue
            resultado_cripto_from = cripto.consultar_cambio()
            resultado_cripto_from = float(resultado_cripto_from)
            resultado_cripto_from *= valor[1]
            resultado_cripto_from = totales_monedas.append(
                resultado_cripto_from)
        suma_valor = sum(totales_monedas)
        return suma_valor



