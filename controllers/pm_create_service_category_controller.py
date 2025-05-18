from entities.service_category_entity import ServiceCategoryEntity
from exceptions import DomainError,CreateError
class PmCreateServiceCategoryController:
    def handle(self, data: dict) -> ServiceCategoryEntity:
        """
        data keys: name, description
        """
        try:
            return ServiceCategoryEntity.create(
                name=data["name"],
                description=data.get("description")
            )
        except CreateError as e:
            raise
