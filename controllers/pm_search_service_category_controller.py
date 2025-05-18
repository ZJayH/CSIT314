from entities.service_category_entity import ServiceCategoryEntity

class PmSearchServiceCategoryController:
    def handle(self, keyword: str) -> list[ServiceCategoryEntity]:
        return ServiceCategoryEntity.search(keyword)