from flask_pymongo import pymongo
import random

def find_horoscope(date, db):
	"""
	Returns sign object for a given birthday
	"""
	day = date[5:]

	sign = db.signs.find_one({"$and":[ {"start":{"$lte":day}}, {"end":{"$gte":day}}]})

	if (sign is None):
		return db.signs.find_one({"name":"Capricorn"})
	# because of using string comparison to find appropriate sign, this fails
	# for capricorn because it wraps around dec to jan. A more sophistocated program
	# would use date objects that took into account the wraparound.

	return sign


def date2string(date):
	"""
	Converts numerical date string into Month and day
	"""

	ind1 = date.find("-")
	ind2 = date.find("-",ind1+1)

	month = date[ind1+1:ind2]
	day = date[ind2+1:]

	month = int(month)

	months = {1:"January",2:"Febuary",3:"March",4:"April",5:"May",6:"June",7:"July",
	8:"August",9:"September",10:"October",11:"November",12:"December"}

	return (months[month] + " " + day)
    

def get_wine(sign,db):
	""" 
	Gets a wine recommendation based on horoscope. 
	Queries for all wines that match sign, and returns random one

	got horoscope recs from:
	https://winefolly.com/lifestyle/wine-zodiac-matching/
	"""

	wine_types = db.signs.find_one({"name":sign})

	query = []

	for wine in wine_types["wines"]:
		query.append({"grape":wine})


	wine_list = list(db.wine.find({"$or":query}))


	return random.choice(wine_list)





