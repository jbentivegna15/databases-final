from flask import Flask, url_for, render_template, redirect, request
from db import connect
import horoscope as h
from flask_pymongo import pymongo

import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

db = connect()

@app.route('/')
def homepage():
    return render_template('homepage.html')
    

@app.route('/results',methods = ['POST','GET','RELOAD'])
def results():
    if request.method == 'POST': 
        if (request.form.get('recommend') == 'Recommend'):

            wine = list(db.wine.find())[0]
            cheese = list(db.cheese.find())[1]


            date = request.form.get('date')
            sign = h.find_horoscope(date)

            date_string = h.date2string(date)
            print(date_string)

            return render_template("results.html",date=date_string,sign=sign,wine=wine,cheese=cheese)
        
        elif (request.form.get('new') == 'pick another date'):
            return redirect(url_for('homepage'))

        else:
            return redirect(url_for('homepage'))

# similar wine page
# similar cheese page

if __name__=='__main__':
    app.run(port=8000)