""" This module is the testing module for available deliveries service """

from unittest.mock import patch, MagicMock

MOCK_OBJECT = MagicMock()

#
#   Success Tests
#


@patch('services.available_deliveries_service.AvailableDelivery')
def test_success_add_delivery(mock_available_delivery):
    """ Test success add delivery as available """
    available_delivery = {
        "_id": "1", "name": "Santiago", "profile_image":
        "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500]}
    new_available_delivery = MagicMock()
    new_available_delivery.save.return_value = available_delivery
    mock_available_delivery.return_value = new_available_delivery

    from src.services import available_deliveries_service

    ret_value = available_deliveries_service.add_available_delivery({
        "_id": "1", "name": "Santiago", "profile_image":
        "https://urlimagen.com", "coordinates": [-58.3772300, -34.6131500]})

    assert ret_value


@patch('services.available_deliveries_service.AvailableDelivery')
def test_success_delete_delivery(mock_available_delivery):
    """ Test success delete delivery as available"""
    available_delivery = {"_id": "1"}
    new_available_delivery = MagicMock()
    new_available_delivery.save.return_value = available_delivery
    mock_available_delivery.return_value = new_available_delivery

    from src.services import available_deliveries_service

    ret_value = available_deliveries_service.delete_available_delivery({"_id": "1"})

    assert ret_value


@patch('services.available_deliveries_service.AvailableDelivery')
def test_success_query_nearby_deliveries(mock_available_delivery):
    """ Test success query nearby deliveries """
    nearby_deliveries = []
    mock_available_delivery.objects = MOCK_OBJECT
    MOCK_OBJECT.get.return_value = nearby_deliveries

    from src.services import available_deliveries_service

    ret_value = available_deliveries_service.query_nearby_deliveries({
        "radius": 5, "coordinates": [-58.3772300, -34.6131500]})

    assert ret_value == nearby_deliveries
