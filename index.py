import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'your secret key'

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template('admin.html')

@app.route('/reserve', methods = ['GET', 'POST'])
def reserve():
    return render_template('reservations.html')

app.run(host='0.0.0.0')