from entities.profile_entity import ProfileEntity

class AdminRolesController:
    def handle(self) -> list[str]:
        """Return all active roles from profiles table."""
        return ProfileEntity.all_roles()

