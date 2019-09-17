""" This module is the testing module for available deliveries service """

import unittest

from services.available_deliveries_service import AvailableDeliveriesService

class DeliveriesDisponiblesServiceTestCase(unittest.TestCase):
    """ This class is the test case for available deliveries service """

    #
    #   Success Tests
    #

    def test_success_add_delivery(self):
        """ Test success add delivery as available """
        service = AvailableDeliveriesService()
        ret_value = service.add_available_delivery({
            "_id": "1", "name": "Santiago", "profile_image": \
            "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500]})

        assert ret_value

    def test_success_query_nearby_deliveries(self):
        """ Test success query nearby deliveries """
        service = AvailableDeliveriesService()
        ret_value = service.query_nearby_deliveries({
            "radius": 5, "coordinates": [-58.3772300, -34.6131500]})

        assert ret_value == []

    def test_success_delete_delivery(self):
        """ Test success delete delivery as available"""
        service = AvailableDeliveriesService()
        ret_value = service.delete_available_delivery({"_id": "1"})

        assert ret_value is None
