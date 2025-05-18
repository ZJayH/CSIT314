# controller/search_service_listings_controller.py
from entities.service_listing_entity import ServiceListingEntity

class CleanerSearchServiceListingsController:
    def handle(self, data: dict):
        """
        data keys:
          - cleaner_id: int
          - keyword:    str
        """
        return ServiceListingEntity.search_by_cleaner(
            cleaner_id = data['cleaner_id'],
            keyword    = data['keyword']
        )
