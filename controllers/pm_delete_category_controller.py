from entities.service_category_entity import ServiceCategoryEntity

class PmDeleteServiceCategoryController:
    def handle(self, sc_id: int) -> None:
        """
        data key: sc_id
        """
        ServiceCategoryEntity.delete(sc_id)