from repositories.database_api import DB

# database collections
COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

class DeliveriesDisponiblesService:

    def agregar_delivery_disponible(self, delivery_data):
        DB.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data)
        return

    def query_deliveries_cercanos(self, query_data):
        # create geospatial query
        # TODO: averiguar sobre geospatial indexes (son necesarios?)
        longitude = query_data['coordinates'][0]
        latitude = query_data['coordinates'][1]
        radius = query_data['radius']
        query = {'coordinates': {'$geoWithin': {'$center': [[longitude, latitude], radius]}}}

        # run the geospatial query
        return DB.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)


    def borrar_delivery_disponible(self, delivery_data):
        DB.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data)
        return