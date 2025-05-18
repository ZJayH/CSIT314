from entities.account_entity import AccountEntity
from exceptions import DomainError,UpdateError

class AdminUpdateAccountController:
    def handle(self, data: dict) -> AccountEntity:
        """
        data keys: id, and any of name,email,phone,role,is_active
        """
        uid = data.get("id")
        updates = {k: data[k] for k in ("name","email","phone","role","is_active") if k in data}
        try:
            return AccountEntity.update(uid, **updates)
        except UpdateError as e:
            raise
