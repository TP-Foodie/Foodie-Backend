from pymongo import MongoClient

class DB(object):

    URI = 'localhost:27017'
    
    #
    #   Initializer de la API de la base de datos.
    #   Inicializa el MongoClient, la base de datos y sus colecciones.
    # 
    @staticmethod     
    def init():
        client = MongoClient(DB.URI,
                     username='app',
                     password='password',
                     authSource='foodie',
                     authMechanism='SCRAM-SHA-1')
        DB.DATABASE = client['foodie']

    @staticmethod
    def agregar_documento(collection, data):
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def encontrar_documento(collection, query):
        return DB.DATABASE[collection].find_one(query)

    @staticmethod
    def encontrar_lista_documentos(collection, query):
        return [doc for doc in DB.DATABASE[collection].find(query)]

    @staticmethod
    def eliminar_documento(collection, query):
        DB.DATABASE[collection].delete_one(query)

    #   elimina todos los docs de una collection
    @staticmethod
    def eliminar_todos_los_documentos(collection):
        DB.DATABASE[collection].delete_many({})