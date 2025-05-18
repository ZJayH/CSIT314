from entities.confirmed_matches_entity import ConfirmedMatchEntity

class HomeSearchHomeownerHistoryController:
    def handle(self, homeowner_id: int, keyword: str):
        """
        """
        return ConfirmedMatchEntity.search_by_homeowner(homeowner_id, keyword)
