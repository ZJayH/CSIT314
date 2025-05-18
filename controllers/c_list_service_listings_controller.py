from entities.service_listing_entity import ServiceListingEntity

class CleanerListServiceListingsController:
    def handle(self, cleaner_id: int) -> list[ServiceListingEntity]:
        """
        """
        return ServiceListingEntity.list_by_cleaner(cleaner_id)