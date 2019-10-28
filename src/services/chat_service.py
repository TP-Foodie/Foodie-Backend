from models.chat import Chat, ChatMessage

def create_chat(chat_data):
    chat = Chat()

    for key in chat_data.keys():
        chat[key] = chat_data[key]

    return chat.save()

def get_chat(_id):
    return Chat.objects.get(id=_id)  # pylint: disable=E1101

def create_chat_message(id_chat, message_data):
    chat_message = ChatMessage()

    print("OK4")
    for key in message_data.keys():
        chat_message[key] = message_data[key]
    chat_message.id_chat = id_chat
    print("OK5")
    return chat_message.save()

def get_chat_messages(id_chat, page, limit):
    return [chat_message for chat_message in ChatMessage.objects(id_chat=id_chat)
            .order_by('-timestamp').skip(page * limit).limit(limit)]  # pylint: disable=E1101
