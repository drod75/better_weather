from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__, static_url_path='/static')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/credits')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    app.run(debug=True)