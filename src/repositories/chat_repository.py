from models.chat import Chat, ChatMessage


def list_all():
    return Chat.objects


def get_chat(chat_id):
    return Chat.objects.get(id=chat_id)


def count():
    return Chat.objects.count()


def create(uid_1, uid_2, id_order):
    return Chat.objects.create(uid_1=uid_1, uid_2=uid_2, id_order=id_order)


def create_chat_message(uid_sender, message, timestamp, id_chat):
    return ChatMessage.objects.create(
        uid_sender=uid_sender, message=message, timestamp=timestamp, id_chat=id_chat
    )


def get_chat_messages(id_chat, page, limit):
    return [chat_message for chat_message in ChatMessage.objects(id_chat=id_chat)
            .order_by('-timestamp').skip(page * limit).limit(limit)]
