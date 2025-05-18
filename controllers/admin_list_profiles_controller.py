# controllers/admin_list_profiles_controller.py

from entities.profile_entity import ProfileEntity
from typing import List

class AdminListProfilesController:
    def handle(self) -> List[ProfileEntity]:
        """
        Return all ProfileEntity ordered by role.
        """
        return ProfileEntity.list_all()
