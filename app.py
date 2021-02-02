from urllib import parse
from flask import Flask,render_template,request
import requests
from urllib.parse import quote
from urllib.request import urlopen
import json
app = Flask(__name__)

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID=587b5ac9901df5018da3cbdc4524a479"
NEWS_URL = "https://newsapi.org/v2/top-headlines?q={0}&apiKey=e9da7b51e58c495bbd6bac0c6329d32b"

@app.route('/')
@app.route('/index')
def index():
    city = request.args.get('city')
    if not city:
        city = requests.get('https://ipinfo.io/').json()['city']
    url = WEATHER_URL.format(quote(city))
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):
        description = parsed['weather'][0]['description']
        temperature = parsed['main']['temp']
        city = parsed['name']
        icon = parsed['weather'][0]['icon']
        country = parsed['sys']['country']
        wind = parsed['wind']['speed']
        humidity = parsed['main']['humidity']
        pressure = parsed['main']['pressure']
        weather = {'description': description,
                    'temperature': temperature,
                    'city': city,
                    'country': country,
                    'icon': icon,
                    'wind': wind,
                    'humidity': humidity,
                    'pressure': pressure
                    }   
    news = [requests.get(NEWS_URL.format("covid&page=1")).json()['articles'][i] for i in range(0,6)]
    return render_template('index.html',weather=weather,news=news,title="Index")

@app.route('/news')
def news():
    tag = request.args.get('search')
    if not tag:
        tag = 'Covid'
    url = NEWS_URL.format(quote(tag))
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = parsed.get('articles')
    return render_template('news.html', news=news,title="News")

@app.route('/about')
def aboutme():
    return render_template('about.html',title="About Me")


if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)