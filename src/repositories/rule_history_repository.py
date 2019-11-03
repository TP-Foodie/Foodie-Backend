from models.rule import RuleHistory


class RuleHistoryRepository:
    def create(self, data):
        return RuleHistory.objects.create(**data)
