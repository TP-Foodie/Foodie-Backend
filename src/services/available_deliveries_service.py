""" This module handles business logic of available deliveries_endpoint """

from repositories.database_api import DB
from my_exceptions.available_deliveries_exceptions import (
    DeliveryAlreadyAvailableException, DeliveryNotAvailableException)
from schemas.available_delivery_schema import AvailableDeliverySchema

# database collection name.
AVAILABLE_DELIVERIES_COLLECTION = 'available_deliveries'

class AvailableDeliveriesService:
    """ This class handles business logic of available_deliveries endpoint """

    def add_available_delivery(self, delivery_disponible_data):
        """ This method handles business logic of POST in available_deliveries endpoint """
        if DB.encontrar_documento(AVAILABLE_DELIVERIES_COLLECTION,
                                  delivery_disponible_data.get_id()) is not None:
            raise DeliveryAlreadyAvailableException('Delivery ya disponible')

        delivery_disponible_schema = AvailableDeliverySchema()
        DB.agregar_documento(AVAILABLE_DELIVERIES_COLLECTION,
                             delivery_disponible_schema.dump(delivery_disponible_data))
        return True

    def query_nearby_deliveries(self, query_data):
        """ This method handles business logic of GET in available_deliveries endpoint """
        # create geospatial query
        longitude = query_data.coordinates[0]
        latitude = query_data.coordinates[1]
        radius = query_data.radius
        query = {'coordinates': {'$geoWithin': {'$center': [[longitude, latitude], radius]}}}

        # run the geospatial query
        return DB.encontrar_lista_documentos(AVAILABLE_DELIVERIES_COLLECTION, query)

    def delete_available_delivery(self, delivery_data):
        """ This method handles business logic of DELETE in available_deliveries endpoint """
        if DB.encontrar_documento(AVAILABLE_DELIVERIES_COLLECTION,
                                  delivery_data.get_id()) is None:
            raise DeliveryNotAvailableException('Delivery no disponible')

        DB.eliminar_documento(AVAILABLE_DELIVERIES_COLLECTION, delivery_data.get_id())
        return True
        