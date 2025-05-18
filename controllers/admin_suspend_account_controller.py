from entities.account_entity import AccountEntity

class AdminSuspendAccountController:
    def handle(self, uid: int) -> AccountEntity:
        AccountEntity.update(uid, is_active=False)