from entities.service_category_entity import ServiceCategoryEntity
from exceptions import DomainError
class PmUpdateServiceCategoryController:
    def handle(self, data: dict) -> ServiceCategoryEntity:
        """
        data keys: id, name, description
        """
        try:
            return ServiceCategoryEntity.update(
                sc_id       = data["id"],
                name        = data["name"],
                description = data.get("description")
            )
        except DomainError as e:
            raise