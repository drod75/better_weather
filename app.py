from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from weather import get_city_health
# from llama import get_response

app = Flask(__name__, static_url_path='/static')

@app.route('/')
@app.route('/home')
def home():
    place = request.args.get("Search")
    data = get_city_health(place)
    if place != None or place != "Search for a city...":
        return render_template('weather.html', content = data)
    else:
        return render_template('home.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    app.run(debug=True)