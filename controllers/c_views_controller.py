from entities.service_listing_entity import ServiceListingEntity

class CleanerViewController:
    def get_views(self, listing_id: int) -> int:
        """
        """
        return ServiceListingEntity.seed_random_views(listing_id)