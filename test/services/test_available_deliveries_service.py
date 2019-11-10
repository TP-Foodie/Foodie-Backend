""" This module is the testing module for available deliveries service """

from unittest.mock import patch, MagicMock

MOCK_OBJECT = MagicMock()

#
#   Success Tests
#


@patch('services.delivery_service.user_repository')
def test_success_query_nearby_deliveries(user_repository):
    """ Test success query nearby deliveries """
    nearby_deliveries = []
    user_repository.get_nearby_available_deliveries.return_value = nearby_deliveries

    from services import delivery_service

    ret_value = delivery_service.query_nearby_deliveries({
        "radius": 5, "coordinates": [-58.3772300, -34.6131500]})

    assert ret_value == nearby_deliveries
