from models.chat import Chat

def create_chat(chat_data):
    chat = Chat()

    for key in chat_data.keys():
        chat[key] = chat_data[key]

    return chat.save()

def get_chat(_id):
    return Chat.objects.get(id=_id)  # pylint: disable=E1101
