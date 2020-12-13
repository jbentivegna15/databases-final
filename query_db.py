from flask_pymongo import pymongo
from data.cheese_categories import SOFT_CHEESES

def connect():
    CONN_STRING = "mongodb+srv://joey:dbpw@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority"

    client = pymongo.MongoClient(CONN_STRING)
    db = client.wine_and_cheese

    return db

db = connect()

print(db.cheese.distinct("location"))

# print(list(db.cheese.find({'texture': { '$in': SOFT_CHEESES}})))