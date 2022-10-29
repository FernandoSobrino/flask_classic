from criptoapp.key import APIKEY
import requests

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

    def __init__(self,origen,destino,cantidad_from):
        """
        Construye un objeto con las monedas origen y destino y
        el cambio obtenido desde CoinAPI inicializado a cero
        """
        self.moneda_origen = origen
        self.moneda_destino = destino
        self.cantidad_from = cantidad_from

    
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
            self.cantidad_to = self.cambio*self.cantidad_from
            return self.cambio,self.cantidad_to

        else:
            raise APIError(
                "Ha ocurrido un error {} {} al consultar la API".format(
                    respuesta.status_code, respuesta.reason
                )
            )

        
