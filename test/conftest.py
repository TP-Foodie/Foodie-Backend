import pytest
from faker import Faker
from faker.providers import person, internet, phone_number
from mongoengine import connect, disconnect

from src.app import APP
from src.models import User
from src.models.order import Order

# pylint: disable=redefined-outer-name
# This is required, pylint doesn't work well with pytest

@pytest.fixture
def fake():
    cfaker = Faker()
    for provider in [person, internet, phone_number]:
        cfaker.add_provider(provider)
    return cfaker


@pytest.fixture
def a_client_user(cfaker):
    return User(
        name=cfaker.first_name(),
        last_name=cfaker.last_name(),
        password=cfaker.prefix(),
        email=cfaker.email(),
        profile_image=cfaker.image_url(),
        phone=cfaker.phone_number(),
        type="CUSTOMER"
    ).save()


@pytest.fixture
def an_order(cfaker, a_client_user):
    return Order(
        number=cfaker.pydecimal(),
        owner=a_client_user
    ).save()


@pytest.fixture
def a_client():
    APP.config['TESTING'] = True
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    client = APP.test_client()

    yield client

    disconnect()
