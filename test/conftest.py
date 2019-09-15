import pytest

from src.models.order import Order


@pytest.fixture
def an_order():
    return Order()
