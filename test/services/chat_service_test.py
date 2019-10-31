import pytest

from repositories import chat_repository
from services import chat_service


@pytest.mark.usefixtures('a_client')
class TestChatService:
    def test_create_chat(self):
        chat_service.create_chat({'uid_1': "a", 'uid_2': "b", "id_order": "c"})

        chat = chat_repository.list_all()[0]

        assert chat.uid_1 == "a"
        assert chat.uid_2 == "b"
        assert chat.id_order == "c"

    def test_list_chat_messages_are_sorted_by_timestamp(self):
        chat_service.create_chat_message(
            "id_chat", {"uid_sender": "a", "message": "1", "timestamp": 1.0}
        )
        chat_service.create_chat_message(
            "id_chat", {"uid_sender": "a", "message": "2", "timestamp": 2.0}
        )

        chat_messages = chat_service.get_chat_messages("id_chat", 0, 50)

        assert chat_messages[0]["timestamp"] == 2.0
        assert chat_messages[1]["timestamp"] == 1.0
