from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED
from schemas.chat_schema import CreateChatSchema, CreateChatMessageSchema
from services import chat_service
from services.auth_service import authenticate

CHATS_BLUEPRINT = Blueprint('chats', __name__)


@CHATS_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = CreateChatSchema()
    chat_data = schema.load(content)

    return jsonify(chat_service.create_chat(chat_data)), HTTP_201_CREATED


@CHATS_BLUEPRINT.route('/<_id>', methods=['GET'])
@authenticate
def get_chat(_id):
    return jsonify(chat_service.get_chat(_id)), HTTP_200_OK


@CHATS_BLUEPRINT.route('/<_id>/messages/', methods=['POST'])
def create_chat_message(_id):
    content = request.get_json()
    schema = CreateChatMessageSchema()
    message_data = schema.load(content)

    message = chat_service.create_chat_message(_id, message_data)

    chat_service.notify_chat_member(_id, message)

    return jsonify(message), HTTP_200_OK


@CHATS_BLUEPRINT.route('/<_id>/messages/', methods=['GET'])
def get_chat_messages(_id):
    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 50))

    return jsonify(
        {
            "page": page,
            "limit": limit,
            "messages": chat_service.get_chat_messages(_id, page, limit)
        }
    ), HTTP_200_OK
