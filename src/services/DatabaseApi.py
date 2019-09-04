from pymongo import MongoClient

class DatabaseApi:

    #
    #   Initializer de la API de la base de datos.
    #   Inicializa el MongoClient, la base de datos y sus colecciones.
    #     
    def __init__(self):
        self.client = MongoClient('localhost:27017',
              username='app',
              password='password',
              authSource='foodie',
              authMechanism='SCRAM-SHA-1')

        self.db = self.client['test-database']
        self.collection_deliveries_disponibles = self.db['deliveries-disponibles']

    #
    #   Metodo que agrega a un delivery (la persona) a la coleccion 
    #   de deliveries disponibles/online para hacer envios.
    #
    def agregarDeliveryComoDisponible(self, deliveryData):
        # deliveryData deberia tener por lo menos la data de auth, su nombre, 
        # su ubicacion y su foto de perfil.
        try:
            # me fijo si ya existe en la db, en la coleccion de deliveries disponibles
            if self.collection_deliveries_disponibles.find_one({'_id': deliveryData.id}):
                return {'status': 403, 'body': 'Already Exists'}

            # agrego al delivery a la coleccion de 
            self.collection_deliveries_disponibles.insert_one(deliveryData)
            return {"status": 201, "body": "Created Succesfully"}
        except KeyError:
            return {"status": 400, "body": "Wrong Parameters"}


    #
    #   Metodo que hace una geospatial query alrededor del usuario (circulo
    #   con centro en el usuario y de radio 5 km) sobre la coleccion de
    #   deliveries disponibles/online.
    #
    #   En caso positivo, devuelve una lista de hasta 10 deliveries disponibles dentro
    #   del circulo descripto anteriormente (y faltaria saber si ordenados de menor
    #   a mayor distancia al centro del circulo)
    #
    def getDeliveriesDisponiblesCercanos(self, queryData):
        # userData deberia tener por lo menos la data de auth del user, su 
        # ubicacion y la distancia maxima al delivery (si es que la elige el usuario).
        try:
            # TODO: averiguar la unidad de medida del within
            # TODO: averiguar (si se puede) como ordenar la query para que devuelva los  
            query = {"loc": {"$within": {"$center": [[queryData.long, queryData.lat], queryData.radius]}}}
            return {"status": 200, "body": [doc for doc in self.collection_deliveries_disponibles.find(query).limit(10)]}
        except KeyError:
            return {"status": 400, "body": "Wrong Parameters"}
    