import json

from test.support.utils import assert_401, assert_200


class TestRuleController:
    def login(self, client, email, password):
        response = client.post(
            '/api/v1/auth/',
            json={'email': email, 'password': password}
        )

        return json.loads(response.data)['token']

    def get_rules(self, client, a_client_user):
        token = self.login(client, a_client_user.email, a_client_user.password)
        return client.get('api/v1/rules/', headers={'Authorization': 'Bearer {}'.format(token)})

    def test_list_rules_fail_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/rules/')
        assert_401(response)

    def test_get_rule_return_rule(self, a_client, a_rule, a_client_user):
        response = self.get_rules(a_client, a_client_user)

        assert_200(response)

        rule = json.loads(response.data)[0]

        assert rule == {
            'id': str(a_rule.id),
            'name': a_rule.name,
            'active': a_rule.active
        }
