from flask import Blueprint, request

from controllers.utils import HTTP_201_CREATED
from logger import log_request_response
from schemas.user_rating_schema import UserRatingSchema
from services.auth_service import authenticate
from services.user_rating_service import UserRatingService

USER_RATING_BLUEPRINT = Blueprint('user_ratings', __name__)

user_rating_service = UserRatingService()  # pylint: disable=invalid-name
user_rating_schema = UserRatingSchema()  # pylint: disable=invalid-name


@USER_RATING_BLUEPRINT.route('/', methods=['POST'])
@log_request_response
@authenticate
def create():
    user_rating_service.create(user_rating_schema.loads(request.json))
    return '', HTTP_201_CREATED
