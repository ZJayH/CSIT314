from entities.service_listing_entity import ServiceListingEntity

class HomeSearchAllServiceListingsController:
    def handle(self,keyword) -> list[ServiceListingEntity]:
        """
        data keys:
          - keyword: str
        """
        return ServiceListingEntity.search_all(keyword)