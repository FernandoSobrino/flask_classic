from flask import Flask

app = Flask(__name__)

app.config.from_prefixed_env()

DB_PATH = 'data/cryptobase.db'

MONEDAS = [("EUR", "Euro"), ("GBP", "Libra"), ("USD", "Dólar"),
           ("ETH", "Ethereum"), ("BNB", "Binance Coin"), ("BTC", "Bitcoin")]
