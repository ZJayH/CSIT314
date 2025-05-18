from entities.confirmed_matches_entity import ConfirmedMatchEntity

class HomeListHomeownerHistoryController:
    def handle(self, homeowner_id: int):
        """
        """
        return ConfirmedMatchEntity.list_by_homeowner(homeowner_id)
