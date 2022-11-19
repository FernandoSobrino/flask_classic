# flask_classic

Nota: Proyecto en curso de app cripto usando CoinApi.

Debe crear previamente un archivo `settings.py` dentro del directorio
criptoapp especificando una `APIKEY`. Si no, no funcionará. Puede crear su
propia apikey en el sitio de [coinAPI](https://www.coinapi.io/pricing?apikey).

La aplicación está actualmente en desarrollo, con lo que algunas funcionalidades
aún no están disponibles. Es posible que detecte algunos errores que aún
no hayan sido solventados. Se acepta cualquier posible crítica constructiva
para mejorarlo e, incluso, si quiere colaborarse en su desarrollo. Toda ayuda
es agradecida :)  


## Para arrancar la aplicación

1. Generar un entorno virtual. Debe realizarse de la siguiente manera:
   
   Situado en el directorio raíz, debe ejecutar los comandos
   `````
   python -m venv env
   `````

2. Active el entorno virtual:
   #### En Windows:
   `````
   .\env\Scripts\activate
   `````

   #### En Mac, Linux:
   `````
   source ./env/bin/activate
   `````

3. Instale las dependencias

   #### Una vez activado el entorno virtual, ejecute el siguiente comando en la shell:
   - Si desea únicamente probar la aplicación:
   ``````
   pip install -r requirements.txt
   ``````

   - Si desea, además, colaborar en su desarrollo, ejecute entonces:
   `````
   pip install -r requirements.dev.txt
   `````


4. Modifique el archivo `.env_template` a `.env` por los siguientes valores:
   ````
   FLASK_APP=run
   FLASK_DEBUG= establezca a true si quiere activar el depurador para desarrollo
   FLASK_SECRET_KEY= genere una clave secreta con varios
   caracteres alfanuméricos
   ````

5. Ejecute el comando `flask run` en su shell para desplegar el servidor y poder ejecutar la app. Conecte
   a la url por defecto que le indique el log de su shell.



