from entities.profile_entity import ProfileEntity

class AdminSuspendProfileController:
    def handle(self, role: str) -> ProfileEntity:
        """
        Suspend the profile (set is_active=False).
        """
        return ProfileEntity.update(role, is_active=False)
