from entities.service_listing_entity import ServiceListingEntity

class CleanerUpdateServiceListingController:
    def handle(self, data: dict):
        return ServiceListingEntity.update(
            listing_id  = data['listing_id'],
            description = data['description'],
            price       = data['price'],
            category_id = data['category_id']
        )