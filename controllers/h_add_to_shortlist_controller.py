# controller/add_to_shortlist_controller.py

from entities.shortlist_entity import ShortlistEntity

class HomeAddToShortlistController:
    def handle(self, homeowner_id: int, listing_id: int):
        """

        """
        return ShortlistEntity.add_to_shortlist(homeowner_id, listing_id)
