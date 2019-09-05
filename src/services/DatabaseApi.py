from pymongo import MongoClient

class DatabaseApi:

    #
    #   Initializer de la API de la base de datos.
    #   Inicializa el MongoClient, la base de datos y sus colecciones.
    #     
    def __init__(self, uri):
        self.client = MongoClient(uri,
              username='app',
              password='password',
              authSource='foodie',
              authMechanism='SCRAM-SHA-1')
        self.db = self.client['foodie']

    def agregar_documento(self, collection, data):
        self.db[collection].insert_one(data)

    def encontrar_documento(self, collection, query):
        return self.db[collection].find_one(query)

    def encontrar_lista_documentos(self, collection, query):
        return [doc for doc in self.db[collection].find(query)]

    def eliminar_documento(self, collection, id_doc):
        self.db[collection].delete_one({'_id': id_doc})