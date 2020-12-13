import requests
import string
import pymongo
import random

username = "dan"#input("username: ")
password = "pass123"#input("password: ")
uri = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)
client = pymongo.MongoClient(uri)

db = client.wine_and_cheese.signs


name = "Libra"


wine_list = ["Champagne", "Chardonnay", "Mencía", "Petit Verdot", \
"Riesling", "Sauvignon Blanc", "Zweigelt","Chablis"]

db.update_one({"name":name},{"$set":{"wines":wine_list}})