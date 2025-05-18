from entities.account_entity import AccountEntity
from exceptions import DuplicateEmailError,CreateError

class AdminCreateAccountController:
    def handle(self, data: dict) -> AccountEntity:
        """
        data keys: name, email, password, phone, role, is_active
        """
        try:
            return AccountEntity.create(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            phone=data.get("phone"),
            role=data.get("role", "homeowner"),
            is_active=data.get("is_active", True)
        )
        except CreateError as e:
            raise 
        
