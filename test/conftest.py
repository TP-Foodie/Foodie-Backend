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
        type="CUSTOMER"
    ).save()


@pytest.fixture
def an_order_factory(fake, a_client_user):
    def create_order(type=Order.NORMAL_TYPE):
        return Order(
            number=fake.pydecimal(),
            owner=a_client_user,
            type=type
        ).save()
    return create_order


@pytest.fixture
def an_order(an_order_factory):
    return an_order_factory()


@pytest.fixture
def a_favor_order(an_order_factory):
    return an_order_factory(Order.FAVOR_TYPE)


@pytest.fixture
def a_client():
    APP.config['TESTING'] = True
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    client = APP.test_client()

    yield client

    disconnect()
