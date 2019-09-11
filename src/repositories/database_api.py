""" This module is the Database API """

from pymongo import MongoClient

class DB:
    """ This class is the Database API """

    URI = 'localhost:27017'

    #
    #   Initializer de la API de la base de datos.
    #   Inicializa el MongoClient, la base de datos y sus colecciones.
    #
    @staticmethod
    def init():
        """ Initializer de la API de la base de datos.
        Inicializa el MongoClient, la base de datos y sus colecciones."""
        client = MongoClient(DB.URI, username='app', password='password', authSource='foodie',
                             authMechanism='SCRAM-SHA-1')
        DB.DATABASE = client['foodie']

    @staticmethod
    def agregar_documento(collection, data):
        """ This method inserts one document """
        DB.DATABASE[collection].insert_one(data)

    @staticmethod
    def encontrar_documento(collection, id_doc):
        """ This method finds one document by id """
        return DB.DATABASE[collection].find_one({"_id": id_doc})

    @staticmethod
    def encontrar_lista_documentos(collection, query):
        """ This method finds many documents """
        return [doc for doc in DB.DATABASE[collection].find(query)]

    @staticmethod
    def eliminar_documento(collection, id_doc):
        """ This method deletes one document by id """
        DB.DATABASE[collection].delete_one({"_id": id_doc})

    @staticmethod
    def eliminar_todos_los_documentos(collection):
        """ This method deletes all the documents in a collection """
        DB.DATABASE[collection].delete_many({})
        