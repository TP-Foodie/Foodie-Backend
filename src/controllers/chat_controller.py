from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED
from schemas.chat_schema import CreateChatSchema, CreateChatMessageSchema
from services import chat_service, user_service, messaging_service

CHATS_BLUEPRINT = Blueprint('chats', __name__)


@CHATS_BLUEPRINT.route('/', methods=['POST'])
def post():
    content = request.get_json()
    schema = CreateChatSchema()
    chat_data = schema.load(content)

    return jsonify(chat_service.create_chat(chat_data)), HTTP_201_CREATED


@CHATS_BLUEPRINT.route('/<_id>', methods=['GET'])
def get_chat(_id):
    return jsonify(chat_service.get_chat(_id)), HTTP_200_OK


@CHATS_BLUEPRINT.route('/<_id>/messages/', methods=['POST'])
def create_chat_message(_id):
    content = request.get_json()
    schema = CreateChatMessageSchema()
    message_data = schema.load(content)

    message = chat_service.create_chat_message(_id, message_data)

    # notify chat member
    chat = chat_service.get_chat(_id)
    id_receiver = ""
    if message["uid_sender"] == chat["uid_1"]:
        id_receiver = chat["uid_2"]
    else:
        id_receiver = chat["uid_1"]

    sender = user_service.get_user(message["uid_sender"])
    receiver = user_service.get_user(id_receiver)
    registration_token = receiver["fcmToken"]

    # message payload.
    message_payload = {
        'title': sender["name"] + sender["last_name"],
        'body': message["message"],
        'channelId': 'Chat Channel',
        'senderId': message["uid_sender"],
        'receiverId': id_receiver,
        'group': _id,
        'timestamp': str(message["timestamp"])
    }

    messaging_service.send_message_to_device(message_payload, registration_token)

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
