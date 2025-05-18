# controllers/admin_list_accounts_controller.py

from entities.account_entity import AccountEntity

class AdminListAccountsController:
    def handle(self) -> list[AccountEntity]:
        
        return AccountEntity.list_all()
