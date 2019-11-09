""" This module is the testing module for available deliveries service """

from unittest.mock import patch, MagicMock

MOCK_OBJECT = MagicMock()

#
#   Success Tests
#


@patch('services.available_deliveries_service.User')
def test_success_query_nearby_deliveries(user):
    """ Test success query nearby deliveries """
    nearby_deliveries = []
    user.objects.return_value = nearby_deliveries

    from services import available_deliveries_service

    ret_value = available_deliveries_service.query_nearby_deliveries({
        "radius": 5, "coordinates": [-58.3772300, -34.6131500]})

    assert ret_value == nearby_deliveries
