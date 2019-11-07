from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from schemas.chat_schema import CreateChatSchema, CreateChatMessageSchema
from services import chat_service
from services.auth_service import authenticate

CHATS_BLUEPRINT = Blueprint('chats', __name__)


@CHATS_BLUEPRINT.route('/', methods=['POST'])
@authenticate
def post(user):
    content = request.get_json()
    schema = CreateChatSchema()
    chat_data = schema.load(content)

    if str(user["id"]) != chat_data["uid_1"] and str(user["id"]) != chat_data["uid_2"]:
        return jsonify({}), HTTP_401_UNAUTHORIZED

    return jsonify(chat_service.create_chat(chat_data)), HTTP_201_CREATED


@CHATS_BLUEPRINT.route('/<_id>', methods=['GET'])
@authenticate
def get_chat(user, _id):
    chat = chat_service.get_chat(_id)

    if str(user["id"]) != chat["uid_1"] and str(user["id"]) != chat["uid_2"]:
        return jsonify({}), HTTP_401_UNAUTHORIZED

    return jsonify(chat), HTTP_200_OK


@CHATS_BLUEPRINT.route('/<_id>/messages/', methods=['POST'])
@authenticate
def create_chat_message(user, _id):
    content = request.get_json()
    schema = CreateChatMessageSchema()
    message_data = schema.load(content)

    chat = chat_service.get_chat(_id)

    if str(user["id"]) != chat["uid_1"] and str(user["id"]) != chat["uid_2"]:
        return jsonify({}), HTTP_401_UNAUTHORIZED

    message = chat_service.create_chat_message(_id, message_data)

    chat_service.notify_chat_member(_id, message)

    return jsonify(message), HTTP_200_OK


@CHATS_BLUEPRINT.route('/<_id>/messages/', methods=['GET'])
@authenticate
def get_chat_messages(user, _id):
    chat = chat_service.get_chat(_id)

    if str(user["id"]) != chat["uid_1"] and str(user["id"]) != chat["uid_2"]:
        return jsonify({}), HTTP_401_UNAUTHORIZED

    page = int(request.args.get("page", 0))
    limit = int(request.args.get("limit", 50))
    list_messages = chat_service.get_chat_messages(_id, page, limit)

    return jsonify(
        {
            "page": page,
            "limit": limit,
            "messages": list_messages
        }
    ), HTTP_200_OK
