import json

import pytest
from faker import Faker
from faker.providers import person, internet, phone_number, geo, address
from flask import Response
from mongoengine import connect, disconnect
from mongomock import ObjectId

from app import APP
from models import User, Place, Coordinates
from models.order import Order, Product
from models.rule import RuleCondition, RuleConsequence, Rule
from services import user_service


# pylint: disable=redefined-outer-name, function-redefined
# This is required, pylint doesn't work well with pytest


@pytest.fixture
def cfaker():
    cfaker = Faker()
    for provider in [person, internet, phone_number, geo, address]:
        cfaker.add_provider(provider)
    return cfaker


@pytest.fixture
def a_customer_user(cfaker, a_location):
    return User(
        name=cfaker.first_name(),
        last_name=cfaker.last_name(),
        password=cfaker.prefix(),
        email=cfaker.email(),
        profile_image=cfaker.image_url(),
        phone=cfaker.phone_number(),
        type="CUSTOMER",
        location=a_location
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
    return Coordinates(latitude=cfaker.latitude(), longitude=cfaker.longitude())


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
def an_order_factory(cfaker, a_customer_user, a_product, a_delivery_user):
    def create_order(order_type=Order.NORMAL_TYPE):
        return Order(
            number=cfaker.pydecimal(),
            owner=a_customer_user.id,
            type=order_type,
            product=a_product.id,
            delivery=a_delivery_user.id
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
def a_client_user(cfaker):
    password = 'password123123'

    user = user_service.create_user({
        'name': cfaker.name(),
        'last_name': cfaker.last_name(),
        'email': cfaker.email(),
        'password': password,
        'profile_image': cfaker.image_url(),
        'phone': cfaker.phone_number(),
        'type': "CUSTOMER"
    })

    user.password = password

    return user


@pytest.fixture
def an_admin_user(a_client_user):
    a_client_user.type = "BACK_OFFICE"
    return a_client_user


@pytest.fixture
def an_object_id():
    return ObjectId()


@pytest.fixture
def a_condition():
    return RuleCondition(
        variable=RuleCondition.USER_REPUTATION,
        operator=RuleCondition.GREATER_THAN,
        condition_value='1'
    )


@pytest.fixture
def a_condition_data(a_condition):
    return a_condition.to_mongo()


@pytest.fixture
def a_consequence_data(a_consequence):
    return a_consequence.to_mongo()


@pytest.fixture
def a_consequence():
    return RuleConsequence(consequence_type=RuleConsequence.VALUE, value=0)


@pytest.fixture
def a_rule(cfaker, a_condition, a_consequence):
    return Rule(
        name=cfaker.name(),
        conditions=[a_condition],
        consequence=a_consequence
    ).save()


@pytest.fixture
def a_city(cfaker):
    return cfaker.city()


class MockedResponse:
    def __init__(self, content):
        self.content = content


@pytest.fixture
def a_geocode_response(a_city):
    return MockedResponse(json.dumps({
        'results': [
            {
                'locations': [
                    {'adminArea5': a_city}
                ]
            }
        ]
    }))
