""" This module handles business logic of deliveries_disponibles endpoint """

from repositories.database_api import DB
from deliveries_disponibles.exceptions import (
    DeliveryYaDisponibleException, DeliveryNoDisponibleException)
from deliveries_disponibles.schemas.delivery_disponible_schema import DeliveryDisponibleSchema

# database collections
COLLECTION_DELIVERIES_DISPONIBLES = 'deliveries_disponibles'

class DeliveriesDisponiblesService:
    """ This class handles business logic of deliveries_disponibles endpoint """

    def agregar_delivery_disponible(self, delivery_disponible_data):
        """ This method handles business logic of POST in deliveries_disponibles endpoint """
        if DB.encontrar_documento(COLLECTION_DELIVERIES_DISPONIBLES,
                                  delivery_disponible_data.get_id()) is not None:
            raise DeliveryYaDisponibleException('Delivery ya disponible')

        delivery_disponible_schema = DeliveryDisponibleSchema()
        DB.agregar_documento(COLLECTION_DELIVERIES_DISPONIBLES,
                             delivery_disponible_schema.dump(delivery_disponible_data))
        return True

    def query_deliveries_cercanos(self, query_data):
        """ This method handles business logic of GET in deliveries_disponibles endpoint """
        # create geospatial query
        longitude = query_data.coordinates[0]
        latitude = query_data.coordinates[1]
        radius = query_data.radius
        query = {'coordinates': {'$geoWithin': {'$center': [[longitude, latitude], radius]}}}

        # run the geospatial query
        return DB.encontrar_lista_documentos(COLLECTION_DELIVERIES_DISPONIBLES, query)

    def eliminar_delivery_disponible(self, delivery_data):
        """ This method handles business logic of DELETE in deliveries_disponibles endpoint """
        if DB.encontrar_documento(COLLECTION_DELIVERIES_DISPONIBLES,
                                  delivery_data.get_id()) is None:
            raise DeliveryNoDisponibleException('Delivery no disponible')

        DB.eliminar_documento(COLLECTION_DELIVERIES_DISPONIBLES, delivery_data.get_id())
        return True
        