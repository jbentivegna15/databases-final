from flask import Flask, url_for, render_template, redirect
from db import connect
from forms import DateForm
from flask_pymongo import pymongo
import random
from get_cheese_recommendation import get_cheese_recommendation
from get_horoscope import get_horoscope

import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = connect()

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = DateForm()
    if form.validate_on_submit():
        return redirect(url_for('results', date=form.date.data))
    return render_template('homepage.html', form=form)

@app.route('/results/<date>', methods=['GET'])
def results(date):
    wine = random.choice(list(db.wine.find()))
    cheese = get_cheese_recommendation(wine, db)
    
    sign = 'Libra'
    horoscope = get_horoscope(sign)

    return render_template('results.html', date=date, wine=wine['name'], cheese=cheese['name'], horoscope=horoscope['horoscope'])

if __name__=='__main__':
    app.run(port=8000)