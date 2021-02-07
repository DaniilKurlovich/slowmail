import pymongo as pym

MONGO_CLIENT = pym.MongoClient('mongodb://slowmail:slowmail@mongo_service', 27017)
db = MONGO_CLIENT['mongo_slowmail']
COLLECTION = db['series']
