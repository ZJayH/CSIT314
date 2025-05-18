from entities.shortlist_entity import ShortlistEntity

class HomeSearchShortlistController:
    def handle(self, homeowner_id: int, keyword: str):
        return ShortlistEntity.search_for_homeowner(homeowner_id, keyword)