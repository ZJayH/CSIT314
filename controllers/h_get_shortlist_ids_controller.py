# controller/get_shortlist_ids_controller.py

from entities.shortlist_entity import ShortlistEntity

class HomeGetShortlistIdsController:
    def handle(self, homeowner_id: int) -> set[int]:
        """
        """
        entries = ShortlistEntity.get_shortlist_for_homeowner(homeowner_id)
        return {s.listing_id for s in entries}
