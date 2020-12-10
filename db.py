from flask_pymongo import pymongo

def connect():
    CONN_STRING = "##MONGO CONNECTION STRING##"

    client = pymongo.MongoClient(CONN_STRING)
    db = client.wine_and_cheese

    return db
    