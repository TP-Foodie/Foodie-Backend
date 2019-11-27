from flask import Blueprint, jsonify, request

from controllers.utils import HTTP_200_OK
from schemas.product_schema import ListProductSchema
from services.auth_service import authenticate
from services import product_service
from logger import log_request_response

PRODUCTS_BLUEPRINT = Blueprint('products', __name__)


@PRODUCTS_BLUEPRINT.route('/', methods=['GET'])
@log_request_response
@authenticate
def get_products():
    id_place = request.args.get('id_place')

    data = ListProductSchema(many=True).dump(
        product_service.get_products_from_place(id_place)
    )

    return jsonify(data), HTTP_200_OK
