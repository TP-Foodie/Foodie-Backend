from test.support.utils import assert_403


class TestRuleController:
    def get_rules(self, client):
        return client.get('api/v1/rules/')

    def test_list_rules_fail_for_unauthenticated(self, a_client):
        response = self.get_rules(a_client)
        assert_403(response)
