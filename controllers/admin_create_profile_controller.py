from entities.profile_entity import ProfileEntity
from exceptions import DomainError,CreateError

class AdminCreateProfileController:
    def handle(self, data: dict) -> ProfileEntity:
        """
        data keys:
          - role: string
          - description: optional string
          - is_active: optional bool
        """
        role = data.get("role", "").strip()
        try:
          return ProfileEntity.create(
              role=role,
              description=data.get("description", ""),
              is_active=data.get("is_active", True)
          )
        except CreateError as e:
            raise
