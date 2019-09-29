import pytest
from faker import Faker
from faker.providers import person, internet, phone_number, geo
from mongoengine import connect, disconnect
from mongomock import ObjectId

from src.app import APP
from src.models import User, Place, Coordinates
from src.models.order import Order, Product


# pylint: disable=redefined-outer-name, function-redefined
# This is required, pylint doesn't work well with pytest
from src.models.rule import RuleCondition


@pytest.fixture
def cfaker():
    cfaker = Faker()
    for provider in [person, internet, phone_number, geo]:
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
def a_delivery_user(cfaker):
    return User(
        name=cfaker.first_name(),
        last_name=cfaker.last_name(),
        password=cfaker.prefix(),
        email=cfaker.email(),
        profile_image=cfaker.image_url(),
        phone=cfaker.phone_number(),
        type="DELIVERY"
    ).save()


@pytest.fixture
def a_location(cfaker):
    return Coordinates(cfaker.latitude(), cfaker.longitude())


@pytest.fixture
def a_place(cfaker, a_location):
    return Place(
        name=cfaker.name(),
        coordinates=a_location
    ).save()


@pytest.fixture
def a_product(cfaker, a_place):
    return Product(
        name=cfaker.name(),
        place=a_place
    ).save()


@pytest.fixture
def an_order(an_order_factory):
    return an_order_factory()


@pytest.fixture
def a_favor_order(an_order_factory):
    return an_order_factory(Order.FAVOR_TYPE)


@pytest.fixture
def an_order_factory(cfaker, a_client_user, a_product):
    def create_order(order_type=Order.NORMAL_TYPE):
        return Order(
            number=cfaker.pydecimal(),
            owner=a_client_user.id,
            type=order_type,
            product=a_product.id
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


@pytest.fixture
def an_object_id():
    return ObjectId()


@pytest.fixture
def a_condition():
    return RuleCondition()
