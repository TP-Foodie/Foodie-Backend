from repositories.database_api import DB
from deliveries_disponibles.exceptions import DeliveryYaDisponibleException, DeliveryNoDisponibleException

# database collections
COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

class DeliveriesDisponiblesService:

    def agregar_delivery_disponible(self, delivery_data):
        if DB.encontrar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data) is not None:
            raise DeliveryYaDisponibleException('Delivery ya disponible')

        DB.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data)
        return True

    def query_deliveries_cercanos(self, query_data):
        # create geospatial query
        # TODO: averiguar sobre geospatial indexes (son necesarios?)
        longitude = query_data.coordinates[0]
        latitude = query_data.coordinates[1]
        radius = query_data.radius
        query = {'coordinates': {'$geoWithin': {'$center': [[longitude, latitude], radius]}}}

        # run the geospatial query
        return DB.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)

    def eliminar_delivery_disponible(self, delivery_data):
        if DB.encontrar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data) is None:
            raise DeliveryNoDisponibleException('Delivery no disponible')

        DB.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data)
        return True
        