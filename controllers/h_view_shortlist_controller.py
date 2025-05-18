from entities.shortlist_entity import ShortlistEntity

class HomeViewShortlistController:
    def handle(self, homeowner_id: int):
        return ShortlistEntity.get_shortlist_for_homeowner(homeowner_id)