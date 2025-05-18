from entities.service_listing_entity import ServiceListingEntity

class HomeListAllServiceListingsController:
    def handle(self) -> list[ServiceListingEntity]:
        return ServiceListingEntity.list_all()