from flask import Blueprint, request, jsonify

from controllers.utils import HTTP_200_OK, HTTP_201_CREATED
from schemas.chat_schema import CreateChatSchema
from services import chat_service

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
