from entities.service_listing_entity import ServiceListingEntity

class CleanerCreateServiceListingController:
    def handle(self, data: dict) -> ServiceListingEntity:
        """
        data keys: cleaner_id, description, price, category_id
        """
        return ServiceListingEntity.create(
            cleaner_id  = data['cleaner_id'],
            description = data['description'],
            price       = data['price'],
            category_id = data['category_id']
        )
