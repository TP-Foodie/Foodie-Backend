from pymongo import MongoClient
from settings import Config

CLIENT = MongoClient(Config.DATABASE_HOST + ':' + Config.DATABASE_PORT,
                     username=Config.DATABASE_USERNAME,
                     password=Config.DATABASE_PASSWORD,
                     authSource=Config.DATABASE_AUTH_SOURCE,
                     authMechanism=Config.DATABASE_AUTH_MECHANISM,
                     ssl=Config.DATABASE_SSL)
