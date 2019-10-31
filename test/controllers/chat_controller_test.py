import json

from test.support.utils import TestMixin, assert_200, assert_401, assert_201
from repositories import chat_repository


class TestChatController(TestMixin):  # pylint: disable=too-many-public-methods
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

    def get_chat(self, client, a_chat, a_client_user):
        self.login(client, a_client_user.email, a_client_user.password)
        return self.get(client, self.build_url('/chats/{}'.format(str(a_chat.id))))

    def test_chats_endpoint_exists(self, a_client, a_chat, a_client_user):
        response = self.get_chat(a_client, a_chat, a_client_user)
        assert_200(response)

    def test_get_chat_for_unauthenticated(self, a_client, a_chat):
        response = a_client.get(self.build_url('/chats/{}'.format(str(a_chat.id))))
        assert_401(response)

    def test_get_chat(self, a_client, a_chat, a_client_user):
        response = self.get_chat(a_client, a_chat, a_client_user)
        assert_200(response)
        chat = json.loads(response.data)

        assert chat == {
            'id': str(a_chat.id),
            'uid_1': a_chat.uid_1,
            'uid_2': a_chat.uid_2,
            'id_order': a_chat.id_order,
        }

    def test_create_chat_for_unauthenticated(self, a_client):
        response = a_client.post('api/v1/chats/', json={"uid_1": "a", "uid_2": "a", "id_order": "a"})
        assert_401(response)

    def test_user_should_be_able_to_create_chat(self, a_client, a_client_user):
        response = self.create_chat(a_client, a_client_user, "a", "b", "c")
        assert_201(response)

    def test_create_chat_should_create_one_on_db(self, a_client, a_client_user):
        self.create_chat(a_client, a_client_user, "a", "b", "c")

        assert chat_repository.count() == 1
