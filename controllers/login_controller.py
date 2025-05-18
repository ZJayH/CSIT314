from entities.account_entity import AccountEntity
from exceptions import DomainError,LoginError

class AdminLoginController:
    def handle(self, data: dict) -> AccountEntity:
        """
        data keys: email, password
        """
        try:
            return AccountEntity.authenticate(
                email=data["email"],
                password=data["password"]
            )
        except LoginError as e:
            raise
