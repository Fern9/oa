from pymongo import MongoClient
from . import settings

# connect to database and get a clinet
client = MongoClient('mongodb://%s:%s@localhost:53382/'%(settings.MONGO_USER, settings.MONGO_PWD))
# switch database to oa
db = client.oa

