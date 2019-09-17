""" This module handles business logic of available deliveries_endpoint """

from models.available_delivery import AvailableDelivery

class AvailableDeliveriesService:
    """ This class handles business logic of available_deliveries endpoint """

    def add_available_delivery(self, available_delivery_data):
        """ This method handles business logic of POST in available_deliveries endpoint """
        available_delivery = AvailableDelivery()

        for key in available_delivery_data.keys():
            available_delivery[key] = available_delivery_data[key]

        available_delivery.save()

        return True

    def query_nearby_deliveries(self, query_data):
        """ This method handles business logic of GET in available_deliveries endpoint """
        # create geospatial query
        longitude = query_data['coordinates'][0]
        latitude = query_data['coordinates'][1]
        radius = query_data['radius']

        return [delivery for delivery in AvailableDelivery.objects(coordinates__geo_within_center=\
                [[longitude, latitude], radius])]

    def delete_available_delivery(self, available_delivery_data):
        """ This method handles business logic of DELETE in available_deliveries endpoint """
        delete_available_delivery = AvailableDelivery()

        for key in available_delivery_data.keys():
            delete_available_delivery[key] = available_delivery_data[key]

        delete_available_delivery.delete()

        return True
        