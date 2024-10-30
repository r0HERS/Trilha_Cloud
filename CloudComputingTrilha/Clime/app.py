import requests
from flask import Flask, render_template, request

app = Flask(__name__)

VIACEP_API_URL = "https://viacep.com.br/ws/{cep}/json/"
METAWEATHER_API_URL = "http://www.metaweather.com/api/location/search/?query={city}"
METAWEATHER_LOCATION_API_URL = "http://www.metaweather.com/api/location/{woeid}/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    cep = request.form['cep']
    
    # Obtém os dados de localização a partir do CEP
    response = requests.get(VIACEP_API_URL.format(cep=cep))
    
    if response.status_code != 200:
        return f"Erro ao buscar o CEP: {response.status_code}"
    
    location_data = response.json()

    if "erro" in location_data:
        return "CEP inválido!"

    city = location_data['localidade']
    
    # Obtém o WOEID (Where On Earth IDentifier) da cidade usando a API MetaWeather
    response = requests.get(METAWEATHER_API_URL.format(city=city), verify=False)
    
    if response.status_code != 200:
        return f"Erro ao buscar clima para a cidade {city}: {response.status_code}"
    
    try:
        weather_location = response.json()
    except requests.exceptions.JSONDecodeError:
        return f"Erro ao decodificar resposta JSON: {response.text}"

    if len(weather_location) == 0:
        return "Localização não encontrada na API de clima."

    woeid = weather_location[0]['woeid']
    
    # Obtém os dados de clima usando o WOEID
    response = requests.get(METAWEATHER_LOCATION_API_URL.format(woeid=woeid), verify=False)

    if response.status_code != 200:
        return f"Erro ao buscar dados climáticos: {response.status_code}"
    
    try:
        weather_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return f"Erro ao decodificar resposta JSON de clima: {response.text}"

    return render_template('weather.html', city=city, weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
