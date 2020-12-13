from flask import Flask, url_for, render_template, redirect, request
from db import connect
import horoscope as h
from flask_pymongo import pymongo
import random
from get_cheese_recommendation import get_cheese_recommendation
from get_horoscope import get_horoscope

import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = connect()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/results', methods = ['POST','GET','RELOAD'])
def results():
    if request.method == 'POST': 
        if (request.form.get('recommend') == 'Recommend'):

            # get date, find horoscope from date, convert date to string
            date = request.form.get('date')
            sign = h.find_horoscope(date,db)
            date_string = h.date2string(date)

            # get wine from horoscope, get cheese from recommendation engine
            wine = h.get_wine(sign["name"],db)
            cheese = get_cheese_recommendation(wine, db)

            # get daily horoscope from API
            horoscope = get_horoscope(sign['name'])

            return render_template("results.html", date=date_string, sign=sign, wine=wine, cheese=cheese, horoscope=horoscope['horoscope'])
        
        elif (request.form.get('new') == 'Pick another date'):
            return redirect(url_for('homepage'))

        else:
            return redirect(url_for('homepage'))

if __name__=='__main__':
    app.run(port=8000)