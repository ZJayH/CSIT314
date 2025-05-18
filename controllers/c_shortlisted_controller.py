from entities.service_listing_entity import ServiceListingEntity

class CleanerShortlistedController:
    def get_shortlist_count(self, listing_id: int) -> int:
        return ServiceListingEntity.refresh_shortlist_count(listing_id)