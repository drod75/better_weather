from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from weather import get_city_health
# from llama import get_response

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def default():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form['city']
        return redirect(url_for('weather', content = city))
    return render_template('home.html')

@app.route('/weather_for_<content>', methods=['GET', 'POST'])
def weather(content):
    data = get_city_health(content)
    return render_template('weather.html', content = data)

@app.route('/credits')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)