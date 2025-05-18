# controllers/list_confirmed_matches_controller.py

from entities.confirmed_matches_entity import ConfirmedMatchEntity

class CleanerListConfirmedMatchesController:
    def handle(self, cleaner_id: int):
        """
        """
        return ConfirmedMatchEntity.list_by_cleaner(cleaner_id)
