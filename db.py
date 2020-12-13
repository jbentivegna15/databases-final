from flask_pymongo import pymongo

def connect():
    username = input("username: ")
    password = input("passord: ")
    CONN_STRING = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)

    client = pymongo.MongoClient(CONN_STRING)
    db = client.wine_and_cheese

    return db
