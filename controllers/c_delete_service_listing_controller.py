from entities.service_listing_entity import ServiceListingEntity

class CleanerDeleteServiceListingController:
    def handle(self, listing_id: int):
        ServiceListingEntity.delete(listing_id)