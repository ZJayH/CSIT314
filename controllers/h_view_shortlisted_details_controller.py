from entities.service_listing_entity import ServiceListingEntity

class HomeownerViewShortlistedListingController:
    def handle(self, homeowner_id: int, listing_id: int):
        listing = ServiceListingEntity.query.get(listing_id)
        
        return listing