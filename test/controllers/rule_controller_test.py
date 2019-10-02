import json

from src.models.rule import Rule
from test.support.utils import assert_401, assert_200, assert_201, assert_400


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

    def get_rule(self, client, a_client_user, a_rule):
        token = self.login(client, a_client_user.email, a_client_user.password)
        return client.get('api/v1/rules/{}'.format(str(a_rule.id)),
                          headers={'Authorization': 'Bearer {}'.format(token)})

    def create_rule(self, client, a_client_user, data):
        token = self.login(client, a_client_user.email, a_client_user.password)
        return client.post(
            'api/v1/rules/',
            json=data,
            headers={'Authorization': 'Bearer {}'.format(token)}
        )

    def test_list_rules_fail_for_unauthenticated(self, a_client):
        response = a_client.get('api/v1/rules/')
        assert_401(response)

    def test_list_rules_returns_all(self, a_client, a_rule, a_client_user):
        response = self.get_rules(a_client, a_client_user)

        assert_200(response)

        rule = json.loads(response.data)[0]

        assert rule == {
            'id': str(a_rule.id),
            'name': a_rule.name,
            'active': a_rule.active
        }

    def test_get_rule_details_fails_for_unauthenticated(self, a_client, a_rule):
        response = a_client.get('api/v1/rules/{}'.format(str(a_rule.id)))
        assert_401(response)

    def test_get_rule_details_return_all_details(self, a_client, a_rule, a_client_user):
        response = self.get_rule(a_client, a_client_user, a_rule)
        assert_200(response)

        rule = json.loads(response.data)

        assert rule == {
            'id': str(a_rule.id),
            'name': a_rule.name,
            'condition': {
                'variable': a_rule.condition.variable,
                'operator': a_rule.condition.operator,
                'condition_value': a_rule.condition.condition_value
            },
            'consequence': {
                'consequence_type': a_rule.consequence.consequence_type,
                'value': a_rule.consequence.value
            },
            'active': a_rule.active
        }

    def test_create_fails_for_unauthenticated(self, a_client):
        response = a_client.post('api/v1/rules/', )

        assert_401(response)

    def test_post_rule_should_create_one(self, a_client, a_client_user, a_consequence_data, a_condition_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'consequence': a_consequence_data,
                'condition': a_condition_data,
                'name': 'a rule'
            }
        )
        assert_201(response)

        assert Rule.objects.count() == 1

    def test_post_rule_should_return_400_if_missing_argument(self, a_client, a_client_user, a_condition_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'condition': a_condition_data,
                'name': 'a rule'
            }
        )
        assert_400(response)

    def test_post_rule_should_return_400_if_arguments_are_wrong(self, a_client, a_client_user):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'consequence': {
                    'consequence_type': 'V',
                    'value': '5'
                },
                'condition': {
                    'variable': 'DOES NOT EXISTS',
                    'operator': 'GTE',
                    'condition_value': '3'
                },
                'name': 'a rule'
            }
        )
        assert_400(response)

    def test_post_rule_should_return_400_if_consequence_values_are_wrong(self, a_client, a_client_user,
                                                                         a_condition_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'consequence': {
                    'consequence_type': 'DOES NOT EXISTS',
                    'value': '5'
                },
                'condition': a_condition_data,
                'name': 'a rule'
            }
        )
        assert_400(response)
