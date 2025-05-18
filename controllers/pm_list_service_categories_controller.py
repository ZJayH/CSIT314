from entities.service_category_entity import ServiceCategoryEntity

class PmListServiceCategoryController:
    def handle(self) -> list[ServiceCategoryEntity]:
        """
        """
        return ServiceCategoryEntity.list_all()