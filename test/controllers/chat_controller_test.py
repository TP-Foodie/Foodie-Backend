#pylint: disable-msg=too-many-arguments
import json

from test.support.utils import TestMixin, assert_200, assert_401, assert_201, assert_404
from repositories import chat_repository


class TestChatController(TestMixin):
    def build_url(self, url):
        return f'/api/v1{url}'

    def create_chat(self, client, user, uid_1, uid_2, id_order):
        self.login(client, user.email, user.password)
        return self.post(
            client,
            self.build_url('/chats/'),
            {
                'uid_1': uid_1,
                'uid_2': uid_2,
                'id_order': id_order
            })

    def create_chat_message(self, client, user, id_chat, uid_sender, message, timestamp):
        self.login(client, user.email, user.password)
        return self.post(
            client,
            self.build_url('/chats/{}/messages/'.format(id_chat)),
            {
                'uid_sender': uid_sender,
                'message': message,
                'timestamp': timestamp
            })

    def get_chat(self, client, id_chat, a_client_user):
        self.login(client, a_client_user.email, a_client_user.password)
        return self.get(client, self.build_url('/chats/{}'.format(id_chat)))

    def get_chat_messages(self, client, a_client_user, id_chat, page, limit):
        self.login(client, a_client_user.email, a_client_user.password)
        return self.get_paging(
            client,
            self.build_url('/chats/{}/messages/'.format(id_chat)),
            page,
            limit
        )

    def test_chats_endpoint_exists(self, a_client, a_client_user):
        response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        assert_201(response)

    def test_get_chat_for_unauthenticated(self, a_client, a_chat):
        response = a_client.get(self.build_url('/chats/{}'.format(str(a_chat.id))))
        assert_401(response)

    def test_get_chat_for_not_chat_member(self, a_client, a_client_user, a_chat):
        response = self.get_chat(a_client, a_chat.id, a_client_user)
        assert_401(response)

    def test_get_chat(self, a_client, a_client_user):
        chat_response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        chat = json.loads(chat_response.data)
        response = self.get_chat(a_client, str(chat["id"]), a_client_user)
        assert_200(response)

        assert chat == {
            'id': str(chat["id"]),
            'uid_1': str(a_client_user.id),
            'uid_2': "b",
            'id_order': "c",
        }

    def test_create_chat_for_unauthenticated(self, a_client):
        response = a_client.post(
            'api/v1/chats/',
            json={"uid_1": "a", "uid_2": "a", "id_order": "a"}
        )
        assert_401(response)

    def test_user_should_be_able_to_create_chat(self, a_client, a_client_user):
        response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        assert_201(response)

    def test_create_chat_should_create_one_on_db(self, a_client, a_client_user):
        self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        assert len(chat_repository.list_all()) == 1

    def test_chat_messages_endpoint_exists(self, a_client, a_client_user):
        chat_response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        chat = json.loads(chat_response.data)
        response = self.get_chat_messages(a_client, a_client_user, str(chat["id"]), 0, 50)
        assert_200(response)

    def test_create_chat_message_for_unauthenticated(self, a_client, a_chat):
        response = a_client.post(
            'api/v1/chats/{}/messages/'.format(str(a_chat.id)),
            json={"uid_sender": "id", "message": "a", "timestamp": 0.0}
        )
        assert_401(response)

    def test_get_chat_messages_for_unauthenticated(self, a_client, a_chat):
        response = a_client.get('api/v1/chats/{}/messages/'.format(str(a_chat.id)))
        assert_401(response)

    def test_create_chat_message_should_create_one_on_db(self, a_client, a_client_user):
        chat_response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        chat = json.loads(chat_response.data)
        self.create_chat_message(a_client, a_client_user, str(chat["id"]), "a", "b", 0.0)
        assert chat_repository.count_chat_messages(str(chat["id"])) == 1

    def test_list_chat_messages(self, a_client, a_client_user):
        chat_response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        chat = json.loads(chat_response.data)
        self.create_chat_message(
            a_client, a_client_user, str(chat["id"]), str(a_client_user.id), "b", 0.0
        )
        response = self.get_chat_messages(
            a_client, a_client_user, str(chat["id"]), 0, 50
        )
        chat_message = json.loads(response.data)["messages"][0]

        assert chat_message['uid_sender'] == str(a_client_user.id)
        assert chat_message['message'] == "b"
        assert chat_message['timestamp'] == 0.0
        assert chat_message['id_chat'] == str(chat["id"])

    def test_list_chat_messages_paging(self, a_client, a_client_user):
        chat_response = self.create_chat(a_client, a_client_user, str(a_client_user.id), "b", "c")
        chat = json.loads(chat_response.data)
        self.create_chat_message(
            a_client, a_client_user, str(chat["id"]), str(a_client_user.id), "1", 1.0
        )
        self.create_chat_message(
            a_client, a_client_user, str(chat["id"]), str(a_client_user.id), "2", 2.0
        )

        assert chat_repository.count_chat_messages(str(chat["id"])) == 2

        response = self.get_chat_messages(
            a_client, a_client_user, str(chat["id"]), 1, 1
        )
        chat_message = json.loads(response.data)["messages"][0]

        assert chat_message["message"] == "2"

    def test_should_return_400_if_chat_does_not_exists(self, a_client, a_client_user, an_object_id):
        self.login(a_client, a_client_user.email, a_client_user.password)
        response = self.get(
            a_client,
            'chats/{}'.format(str(an_object_id))
        )
        assert_404(response)
