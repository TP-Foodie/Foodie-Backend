from pymongo import MongoClient

client = MongoClient('localhost:27017',
                     username='app',
                     password='password',
                     authSource='foodie',
                     authMechanism='SCRAM-SHA-1')
