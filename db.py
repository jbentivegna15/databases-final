from flask_pymongo import pymongo

def connect():
    CONN_STRING = "mongodb+srv://joey:dbpw@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority"

    client = pymongo.MongoClient(CONN_STRING)
    db = client.wine_and_cheese

    return db
    