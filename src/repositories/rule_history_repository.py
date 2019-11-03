from models.rule import RuleHistory


class RuleHistoryRepository:
    def create(self, rule_id, version):
        return RuleHistory.objects.create(versions=[version], rule=rule_id)

    def get_for(self, rule_id):
        return RuleHistory.objects.filter(rule=rule_id).first()
