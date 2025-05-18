# controller/remove_from_shortlist_controller.py

from entities.shortlist_entity import ShortlistEntity

class HomeRemoveFromShortlistController:
    def handle(self, homeowner_id: int, listing_id: int):
        """
        从 homeowner 的短名单中移除某个 listing，
        如果不存在则抛 ValueError。
        """
        return ShortlistEntity.remove_from_shortlist(homeowner_id, listing_id)
