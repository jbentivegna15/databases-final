from flask_pymongo import pymongo

def find_horoscope(date):
	username = input("username: ")
	password = input("passord: ")
	CONN_STRING = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)

	client = pymongo.MongoClient(CONN_STRING)
	db = client.wine_and_cheese.signs

	day = date[5:]

	sign = db.find_one({"$and":[ {"start":{"$lte":day}}, {"end":{"$gte":day}}]})

	if (sign is None):
		return db.find_one({"name":"Capricorn"})

	return sign


def date2string(date):

	ind1 = date.find("-")
	ind2 = date.find("-",ind1+1)

	month = date[ind1+1:ind2]
	day = date[ind2+1:]

	month = int(month)

	months = {1:"January",2:"Febuary",3:"March",4:"April",5:"May",6:"June",7:"July",
	8:"August",9:"September",10:"October",11:"November",12:"December"}

	return (months[month] + " " + day)
    




