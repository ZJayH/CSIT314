from entities.service_listing_entity import ServiceListingEntity

class CleanerListingDetailsController:
    """
    Fetches a single ServiceListingEntity by ID and checks ownership.
    """

    def handle(self, cleaner_id: int, listing_id: int) -> ServiceListingEntity:
        return ServiceListingEntity.list_one(listing_id)