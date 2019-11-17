from repositories import chat_repository, user_repository, messaging_repository


def create_chat(chat_data):
    return chat_repository.create(
        chat_data["uid_1"], chat_data["uid_2"], chat_data["id_order"]
    )


def get_chat(_id):
    return chat_repository.get_chat(_id)


def create_chat_message(id_chat, message_data):
    # increment messages sent by user
    user_repository.increment_messages_sent(message_data["uid_sender"])

    return chat_repository.create_chat_message(
        message_data["uid_sender"], message_data["message"], message_data["timestamp"], id_chat
    )


def get_chat_messages(id_chat, page, limit):
    return chat_repository.get_chat_messages(id_chat, page, limit)


def notify_chat_member(id_chat, message):
    # get chat data
    chat = get_chat(id_chat)
    id_receiver = ""
    if message["uid_sender"] == chat["uid_1"]:
        id_receiver = chat["uid_2"]
    else:
        id_receiver = chat["uid_1"]

    # get chat members data
    sender = user_repository.get_user(message["uid_sender"])
    receiver = user_repository.get_user(id_receiver)
    registration_token = receiver["fcmToken"]

    # notification payload.
    message_payload = {
        'title': sender["name"] + sender["last_name"],
        'body': message["message"],
        'channelId': 'Chat Channel',
        'senderId': message["uid_sender"],
        'senderProfileImage': sender["profile_image"],
        'receiverId': id_receiver,
        'group': id_chat,
        'timestamp': str(message["timestamp"])
    }

    messaging_repository.send_message_to_device(message_payload, registration_token)
