from models.rule import RuleHistory


class RuleHistoryRepository:
    def create(self, version):
        return RuleHistory.objects.create(versions=[version])
