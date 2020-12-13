import requests
import string
from bs4 import BeautifulSoup as bs
import pymongo
import random

username = input("username: ")
password = input("password: ")
uri = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)
client = pymongo.MongoClient(uri)

db = client.wine_and_cheese.wine

# round(random.uniform(8,15),1)

# for doc in db.find():
# 	db.update_one({'_id': doc['_id']},{'$set': {'abv':round(random.uniform(9,20),1)} })

db.update_many( {}, { "$rename": { "Grape Variety": "grape" } } )