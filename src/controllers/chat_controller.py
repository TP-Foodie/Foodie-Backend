from flask import Blueprint, request, jsonify
from flask_socketio import join_room, leave_room
from firebase_admin import messaging
from app import socketio
import logger

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED
from schemas.chat_schema import CreateChatSchema, CreateChatMessageSchema
from services import chat_service, user_service

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

    # notify chat members
    socketio.emit(
        'new_message',
        {"uid_sender": message["uid_sender"], "message": message["message"],
         "timestamp": message["timestamp"], "id_chat": message["id_chat"],
         "id": str(message["id"])}, room=_id, namespace='/chat')

    # This registration token comes from the client FCM SDKs.
    chat = chat_service.get_chat(_id)
    id_receiver = ""
    if message["uid_sender"] == chat["uid_1"]:
        id_receiver = chat["uid_2"]
    else:
        id_receiver = chat["uid_1"]

    sender = user_service.get_user(message["uid_sender"])
    receiver = user_service.get_user(id_receiver)
    registration_token = receiver["fcmToken"]

    # See documentation on defining a message payload.
    fcm_message = messaging.Message(
        data={
            'title': sender["name"] + sender["last_name"],
            'body': message["message"],
            'channelId': 'Chat Channel',
            'senderId': message["uid_sender"],
            'receiverId': id_receiver,
            'group': _id
        },
        token=registration_token,
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(fcm_message)
    # Response is a message ID string.
    logger.warn('Successfully sent message:' + response)

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

@socketio.on('joined', namespace='/chat')
def joined(data):
    """Sent by clients when they enter a room."""
    room = data['id_chat']
    join_room(room)

@socketio.on('left', namespace='/chat')
def left(data):
    """Sent by clients when they leave a room."""
    room = data['id_chat']
    leave_room(room)
