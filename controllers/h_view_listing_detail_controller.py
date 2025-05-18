from entities.service_listing_entity import ServiceListingEntity

class HomeoViewListingDetailController:
    """
    Fetches a single ServiceListingEntity by ID—raises ValueError if not found.
    """

    def handle(self, listing_id: int) -> ServiceListingEntity:
        listing = ServiceListingEntity.query.get(listing_id)
        
        return listing