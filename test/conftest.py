import pytest
from faker import Faker
from faker.providers import person, internet, phone_number

from src.models import User
from src.models.order import Order, OrderStatus, OrderType


@pytest.fixture
def fake():
    fake = Faker()
    for provider in [person, internet, phone_number]:
        fake.add_provider(provider)
    return fake


@pytest.fixture
def an_order_status():
    return OrderStatus()


@pytest.fixture
def an_order_type():
    return OrderType()


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
def an_order(fake, an_order_status, an_order_type, a_client_user):
    return Order(
        number=fake.pydecimal(),
        status=an_order_status,
        type=an_order_type,
        owner=a_client_user
    )
