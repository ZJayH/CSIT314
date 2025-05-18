from entities.confirmed_matches_entity import ConfirmedMatchEntity

class CleanerConfirmedMatchDetailController:
    """
    Returns one ConfirmedMatchEntity if it exists and belongs to this cleaner.
    """

    def handle(self, cleaner_id: int, match_id: int) -> ConfirmedMatchEntity:        
        return ConfirmedMatchEntity.list_one(match_id)