# controllers/admin_update_profile_controller.py

from entities.profile_entity import ProfileEntity

class AdminUpdateProfileController:
    def handle(self, data: dict) -> ProfileEntity:

        role    = data['role']
        updates = {
            k: data[k]
            for k in ('description','is_active')
            if k in data
        }
        return ProfileEntity.update(role, **updates)
