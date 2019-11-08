from models.rule import RuleHistory


class RuleHistoryRepository:
    def create(self, rule_id, version=None):
        return RuleHistory.objects.create(versions=[version] if version else [], rule=rule_id)

    def get_for(self, rule_id):
        return RuleHistory.objects.filter(rule=rule_id).first()
