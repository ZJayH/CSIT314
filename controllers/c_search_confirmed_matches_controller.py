# controllers/search_confirmed_matches_controller.py

from entities.confirmed_matches_entity import ConfirmedMatchEntity


class CleanerSearchConfirmedMatchesController:
    def handle(self, cleaner_id: int, keyword: str):
        # 
        return ConfirmedMatchEntity.search_by_cleaner(cleaner_id, keyword)
