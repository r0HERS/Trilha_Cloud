from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL da API do CoinGecko para pegar os preços das criptomoedas
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Criptomoedas suportadas
CRYPTOS = ['bitcoin', 'ethereum', 'ripple']

# Moedas suportadas
CURRENCIES = ['usd', 'eur', 'brl']

@app.route('/')
def index():
    return render_template('crypto.html', cryptos=CRYPTOS, currencies=CURRENCIES)

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = float(request.form['amount'])
    
    if from_currency in CURRENCIES and to_currency in CRYPTOS:
        # Conversão de moeda tradicional para criptomoeda
        response = requests.get(f"{CRYPTO_API_URL}?ids={to_currency}&vs_currencies={from_currency}")
        data = response.json()
        rate = data[to_currency][from_currency]
        total_crypto = amount / rate
        return render_template('crypto.html', total=total_crypto, currency=to_currency, amount=amount, from_currency=from_currency, cryptos=CRYPTOS, currencies=CURRENCIES)
    
    elif from_currency in CRYPTOS and to_currency in CURRENCIES:
        # Conversão de criptomoeda para moeda tradicional
        response = requests.get(f"{CRYPTO_API_URL}?ids={from_currency}&vs_currencies={to_currency}")
        data = response.json()
        rate = data[from_currency][to_currency]
        total_fiat = amount * rate
        return render_template('crypto.html', total=total_fiat, currency=to_currency, amount=amount, from_currency=from_currency, cryptos=CRYPTOS, currencies=CURRENCIES)
    
    else:
        return "Erro: Conversão não suportada"

if __name__ == '__main__':
    app.run(debug=True)
