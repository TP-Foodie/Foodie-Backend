import pytest
from faker import Faker
from faker.providers import person, internet, phone_number
from mongoengine import connect, disconnect

from src.app import APP
from src.models import User
from src.models.order import Order


@pytest.fixture
def fake():
    fake = Faker()
    for provider in [person, internet, phone_number]:
        fake.add_provider(provider)
    return fake


@pytest.fixture
def a_client_user(fake):
    return User(
        name=fake.first_name(),
        last_name=fake.last_name(),
        password=fake.prefix(),
        email=fake.email(),
        profile_image=fake.image_url(),
        phone=fake.phone_number(),
    )


@pytest.fixture
def an_order(fake, a_client_user):
    return Order(
        number=fake.pydecimal(),
        owner=a_client_user
    )


@pytest.fixture
def a_client():
    APP.config['TESTING'] = True
    connect('mongoenginetest', host='mongomock://localhost', alias='testing')
    client = APP.test_client()

    yield client

    disconnect()
