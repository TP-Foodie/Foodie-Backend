from flask import Blueprint, jsonify, request

from controllers.utils import HTTP_403_FORBIDDEN, HTTP_201_CREATED, HTTP_200_OK
from schemas.product_schema import ProductSchema, ListProductSchema
from services.auth_service import authenticate
from services import product_service
from logger import log_request_response
from models import User

PRODUCTS_BLUEPRINT = Blueprint('products', __name__)


@PRODUCTS_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
@authenticate
def post(user):
    if user.type != User.BACK_OFFICE_TYPE:
        return jsonify({}), HTTP_403_FORBIDDEN

    content = request.get_json()
    schema = ProductSchema()
    product_data = schema.load(content)

    return jsonify(product_service.create_product(product_data)), HTTP_201_CREATED


@PRODUCTS_BLUEPRINT.route('/', methods=['GET'])
@log_request_response
@authenticate
def get_products():
    id_place = request.args.get('id_place')

    data = ListProductSchema(many=True).dump(
        product_service.get_products_from_place(id_place)
    )

    return jsonify(data), HTTP_200_OK
