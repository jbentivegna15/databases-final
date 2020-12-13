from flask_pymongo import pymongo

def connect():
    """
    This function connects to our mongodb atlas database

    Accepts username and password as input and returns the db connection
    to our wine_and_cheese database
    """
    username = input("username: ")
    password = input("passord: ")
    CONN_STRING = "mongodb+srv://{}:{}@datacluster.htvsb.mongodb.net/wine_and_cheese?retryWrites=true&w=majority".format(username,password)

    client = pymongo.MongoClient(CONN_STRING)
    db = client.wine_and_cheese

    return db
