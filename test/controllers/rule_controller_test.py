import json

from test.support.utils import assert_401, assert_200, assert_201, assert_400
from src.models.rule import Rule, RuleCondition


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

    def update_rule(self, client, client_user, rule, new_data):
        token = self.login(client, client_user.email, client_user.password)
        return client.patch(
            'api/v1/rules/{}'.format(str(rule.id)),
            json=new_data,
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
            'conditions': [{
                'variable': a_rule.conditions[0].variable,
                'operator': a_rule.conditions[0].operator,
                'condition_value': a_rule.conditions[0].condition_value
            }],
            'consequence': {
                'consequence_type': a_rule.consequence.consequence_type,
                'value': a_rule.consequence.value
            },
            'active': a_rule.active
        }

    def test_create_fails_for_unauthenticated(self, a_client):
        response = a_client.post('api/v1/rules/', )

        assert_401(response)

    def test_post_rule_should_create_one(self, a_client, a_client_user, a_consequence_data,
                                         a_condition_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'consequence': a_consequence_data,
                'conditions': [a_condition_data],
                'name': 'a rule'
            }
        )
        assert_201(response)

        assert Rule.objects.count() == 1

    def test_post_rule_should_return_400_if_missing_argument(self, a_client, a_client_user,
                                                             a_condition_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'conditions': [a_condition_data],
                'name': 'a rule'
            }
        )
        assert_400(response)

    def test_post_rule_should_return_400_if_arguments_are_wrong(self, a_client,
                                                                a_client_user):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'consequence': {
                    'consequence_type': 'V',
                    'value': '5'
                },
                'conditions': [{
                    'variable': 'DOES NOT EXISTS',
                    'operator': 'GTE',
                    'condition_value': '3'
                }],
                'name': 'a rule'
            }
        )
        assert_400(response)

    def test_post_rule_should_return_400_if_consequence_values_are_wrong(self, a_client,
                                                                         a_client_user,
                                                                         a_condition_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'consequence': {
                    'consequence_type': 'DOES NOT EXISTS',
                    'value': '5'
                },
                'conditions': [a_condition_data],
                'name': 'a rule'
            }
        )
        assert_400(response)

    def test_create_rule_should_return_newly_created(self, a_client, a_client_user,
                                                     a_condition_data, a_consequence_data):
        response = self.create_rule(
            a_client,
            a_client_user,
            {
                'conditions': [a_condition_data],
                'consequence': a_consequence_data,
                'name': 'a rule'
            }
        )

        assert_201(response)

        rule = json.loads(response.data)

        assert rule

    def test_update_field_for_unauthorized(self, a_client, a_rule):
        response = a_client.patch('api/v1/rules/{}'.format(str(a_rule.id)))
        assert_401(response)

    def test_patch_field_should_update_it(self, a_client, a_client_user, a_rule):
        response = self.update_rule(
            a_client,
            a_client_user,
            a_rule,
            {'conditions': [{'variable': RuleCondition.ORDER_DISTANCE}]}
        )

        assert_200(response)

        assert Rule.objects.get(id=a_rule.id).conditions[0].variable == RuleCondition.ORDER_DISTANCE

    def test_patch_field_with_wrong_value_returns_400(self, a_client, a_client_user, a_rule):
        response = self.update_rule(
            a_client,
            a_client_user,
            a_rule,
            {'conditions': [{'variable': 'DOES NOT EXISTS'}]}
        )

        assert_400(response)

    def test_patch_field_should_return_updated_object(self, a_client, a_client_user, a_rule):
        response = self.update_rule(
            a_client,
            a_client_user,
            a_rule,
            {'name': 'new name'}
        )

        assert json.loads(response.data)
