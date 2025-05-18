# controllers/admin_search_profiles_controller.py

from entities.profile_entity import ProfileEntity
from extensions import db

class AdminSearchProfilesController:
    def handle(self, keyword: str) -> list[ProfileEntity]:
        
        return ProfileEntity.search(keyword)

