from flask import Flask, url_for, render_template, redirect
from db import connect
from forms import DateForm
from flask_pymongo import pymongo

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
    wine = list(db.wine.find())[0]['name']
    cheese = list(db.cheese.find())[0]['name']
    # wine_result, cheese_result = get_recommendation(date, db)
    # format_results()
    return render_template('results.html', date=date, wine=wine, cheese=cheese)

# similar wine page
# similar cheese page

if __name__=='__main__':
    app.run(port=8000)